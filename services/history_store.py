import os
from datetime import datetime

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DEFAULT_DB_CONFIG = {
    "dbname": os.getenv("PGDATABASE"),
    "user": os.getenv("PGUSER"),
    "password": os.getenv("PGPASSWORD"),
    "host": os.getenv("PGHOST"),
    "port": int(os.getenv("PGPORT")),
}


def get_connection():
    return psycopg2.connect(**DEFAULT_DB_CONFIG)


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS translations (
                    id SERIAL PRIMARY KEY,
                    input_code TEXT NOT NULL,
                    output_code TEXT NOT NULL,
                    explanation TEXT,
                    target_lang VARCHAR(30) NOT NULL,
                    optimize BOOLEAN NOT NULL DEFAULT FALSE,
                    explain BOOLEAN NOT NULL DEFAULT FALSE,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW()
                );
                """
            )


def save_translation(
    input_code: str,
    output_code: str,
    explanation: str,
    target_lang: str,
    optimize: bool,
    explain: bool,
) -> int:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO translations (input_code, output_code, explanation, target_lang, optimize, explain)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (input_code, output_code, explanation, target_lang, optimize, explain),
            )
            return cursor.fetchone()[0]


def list_translations() -> list[dict]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT id, target_lang, optimize, explain, created_at, output_code, explanation
                FROM translations
                ORDER BY created_at DESC;
                """
            )
            rows = cursor.fetchall()
            for row in rows:
                row["created_at"] = _format_dt(row["created_at"])
                row["preview"] = _build_preview(row["output_code"], row["explanation"])
            return rows


def get_translation(entry_id: int) -> dict | None:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT id, input_code, output_code, explanation, target_lang, optimize, explain, created_at
                FROM translations
                WHERE id = %s;
                """,
                (entry_id,),
            )
            row = cursor.fetchone()
            if not row:
                return None
            row["created_at"] = _format_dt(row["created_at"])
            return row


def _build_preview(code: str, explanation: str | None) -> str:
    combined = f"{code}\\n{explanation or ''}".strip()
    return (combined[:140] + "...") if len(combined) > 140 else combined


def _format_dt(value: datetime) -> str:
    return value.strftime("%Y-%m-%d %H:%M")