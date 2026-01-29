# FanIA

**Traductor inteligente de código C# a múltiples lenguajes**

FanIA es una aplicación web que permite traducir código C# a otros lenguajes de programación (Python, JavaScript, TypeScript, Java y Go) utilizando **Google Gemini**. El sistema puede optimizar el código, corregir errores y generar una explicación línea por línea. Incluye un historial persistente almacenado en **PostgreSQL**.

---

## Funcionamiento general del sistema

FanIA está compuesto por cuatro capas principales:

- **Frontend** (HTML, CSS, JavaScript)
- **Backend** (Flask, API REST)
- **Inteligencia Artificial** (Google Gemini)
- **Base de datos** (PostgreSQL)

**Flujo general:**
1. El usuario ingresa código C# en la interfaz web.
2. El frontend envía los datos al backend mediante JSON.
3. El backend valida la entrada y construye un prompt.
4. Google Gemini genera la traducción.
5. El resultado se guarda en PostgreSQL.
6. El frontend muestra el código traducido y la explicación.

---

## Interfaz (Frontend)

**Ubicación de archivos:**
- `/templates/index.html`
- `/static/css/styles.css`
- `/static/js/app.js`

**Funciones principales:**
- Editor de código C# con CodeMirror.
- Selección de lenguaje destino.
- Opciones de optimización y explicación.
- Visualización del código traducido.
- Caja de explicación.
- Historial de traducciones.
- Botón para copiar el código resultante.

El frontend se comunica con el backend usando **fetch** y JSON.

---

## Backend (Flask)

**Archivo principal:**
- `app.py`

**Responsabilidades del backend:**
- Validar las entradas del usuario.
- Controlar errores.
- Llamar a la API de Google Gemini.
- Guardar y recuperar datos desde PostgreSQL.

---

## 🔌 Endpoints

### `GET /`
Devuelve la interfaz web principal.

### `POST /translate`
Traduce el código C# enviado por el usuario.

**Entrada JSON:**
```json
{
  "code": "...",
  "target_lang": "Python",
  "optimize": true,
  "explain": false
}
```

**Proceso:**
- Valida que el código no esté vacío y sea C#.
- Construye un prompt estricto.
- Llama a Google Gemini.
- Guarda el resultado en PostgreSQL.
- Devuelve el código traducido y la explicación si corresponde.

### `GET /history`
Devuelve la lista del historial de traducciones.

### `GET /history/<id>`
Devuelve el detalle de una traducción específica.

---

## Inteligencia Artificial (Google Gemini)

**Ubicación:**
- `/services/gemini_client.py`
- `/services/translator.py`

**Funciones:**
- `GeminiClient` maneja la conexión con la API de Google Gemini y controla errores.
- `translator.py` construye el prompt y valida que el código de entrada sea C#.

**Reglas principales del prompt:**
- Mantener la lógica original.
- No inventar código.
- Optimizar solo si el usuario lo solicita.
- Explicar solo si la opción está activa.

---

## Base de datos (PostgreSQL)

**Ubicación:**
- `/services/history_store.py`

La base de datos almacena:
- Código original.
- Código traducido.
- Explicación.
- Lenguaje destino.
- Opciones activadas.
- Fecha de creación.

**Tabla principal:** `translations`

---

## Variables de entorno

**Archivo:** `.env`

**Ejemplo:**
```env
GEMINI_API_KEY=your_gemini_api_key_here
PGDATABASE=yourDatabase
PGUSER=postgres
PGPASSWORD=yourPassword
PGHOST=localhost
PGPORT=5432
```

---

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Ejecución

```bash
python app.py
```

Abrir en el navegador:
```
http://localhost:5000
```

---

## Características principales

- Traducción automática de C# a múltiples lenguajes.
- Optimización opcional del código.
- Explicación línea por línea.
- Historial persistente en PostgreSQL.