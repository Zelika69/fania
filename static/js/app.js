const translateBtn = document.getElementById("translateBtn");
const loader = document.getElementById("loader");
const toastEl = document.getElementById("appToast");
const toastBody = document.getElementById("toastBody");
const copyBtn = document.getElementById("copyBtn");
const explanationBox = document.getElementById("explanation");
const historyList = document.getElementById("historyList");
const historyCount = document.getElementById("historyCount");
const historyDetail = document.getElementById("historyDetail");
const historyMeta = document.getElementById("historyMeta");
const historyCode = document.getElementById("historyCode");
const historyExplanation = document.getElementById("historyExplanation");
const closeHistory = document.getElementById("closeHistory");

const toast = new bootstrap.Toast(toastEl, { delay: 4000 });

const inputEditor = CodeMirror.fromTextArea(document.getElementById("codeInput"), {
  mode: "text/x-csharp",
  theme: "material-darker",
  lineNumbers: true,
  lineWrapping: true,
});

const outputEditor = CodeMirror.fromTextArea(document.getElementById("codeOutput"), {
  mode: "text/plain",
  theme: "material-darker",
  lineNumbers: true,
  lineWrapping: true,
  readOnly: true,
});

const showToast = (message, variant = "danger") => {
  toastEl.classList.remove("text-bg-danger", "text-bg-success");
  toastEl.classList.add(`text-bg-${variant}`);
  toastBody.textContent = message;
  toast.show();
};

const setLoading = (isLoading) => {
  loader.classList.toggle("d-none", !isLoading);
  translateBtn.disabled = isLoading;
  translateBtn.textContent = isLoading ? "Traduciendo..." : "Traducir";
};

const renderHistory = (entries) => {
  historyList.innerHTML = "";
  historyCount.textContent = entries.length;

  if (!entries.length) {
    historyList.innerHTML = '<div class="history-empty">Sin historial aún.</div>';
    return;
  }

  entries.forEach((entry) => {
    const item = document.createElement("div");
    item.className = "history-item";
    item.dataset.entryId = entry.id;

    item.innerHTML = `
      <div class="history-meta">
        <span>${entry.target_lang} ${entry.optimize ? "• Optimizado" : ""}</span>
        <span>${entry.created_at}</span>
      </div>
      <div class="history-preview">${entry.preview || "Sin vista previa."}</div>
    `;

    item.addEventListener("click", () => openHistoryDetail(entry.id));
    historyList.appendChild(item);
  });
};

const fetchHistory = async () => {
  try {
    const response = await fetch("/history");
    const data = await response.json();
    if (!response.ok || !data.success) {
      throw new Error(data.message || "No se pudo cargar el historial.");
    }
    renderHistory(data.entries || []);
  } catch (error) {
    showToast(error.message || "No se pudo cargar el historial.");
  }
};

const openHistoryDetail = async (entryId) => {
  historyDetail.classList.remove("d-none");
  historyMeta.textContent = "Cargando...";
  historyCode.textContent = "";
  historyExplanation.textContent = "";

  try {
    const response = await fetch(`/history/${entryId}`);
    const data = await response.json();
    if (!response.ok || !data.success) {
      throw new Error(data.message || "No se pudo cargar el historial.");
    }

    historyMeta.textContent = `${data.entry.target_lang} • ${data.entry.created_at}`;
    historyCode.textContent = data.entry.output_code || "";
    historyExplanation.textContent = data.entry.explanation || "Sin explicación.";
  } catch (error) {
    showToast(error.message || "No se pudo cargar el historial.");
  }
};

const closeHistoryDetail = () => {
  historyDetail.classList.add("d-none");
};

closeHistory.addEventListener("click", closeHistoryDetail);
historyDetail.addEventListener("click", (event) => {
  if (event.target === historyDetail) {
    closeHistoryDetail();
  }
});

translateBtn.addEventListener("click", async () => {
  const codeValue = inputEditor.getValue();
  if (!codeValue.trim()) {
    showToast("El código está vacío. Pega tu código C#.");
    return;
  }
  if (codeValue.length > 6000) {
    showToast("El código supera el límite de 6000 caracteres.");
    return;
  }

  const payload = {
    code: codeValue,
    target_lang: document.getElementById("targetLang").value,
    optimize: document.getElementById("optimize").checked,
    explain: document.getElementById("explain").checked,
  };

  setLoading(true);
  explanationBox.textContent = "Sin explicación.";

  try {
    const response = await fetch("/translate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    if (!response.ok || !data.success) {
      throw new Error(data.message || "Error inesperado.");
    }

    const modeMap = {
      Python: "python",
      JavaScript: "javascript",
      TypeScript: "javascript",
      Java: "text/x-java",
      Go: "text/x-go",
    };
    const target = payload.target_lang;
    outputEditor.setOption("mode", modeMap[target] || "text/plain");
    outputEditor.setValue(data.code || "");
    explanationBox.textContent = data.explanation || "Sin explicación.";
    showToast("Traducción completada.", "success");
    fetchHistory();
  } catch (error) {
    showToast(error.message || "No se pudo traducir.");
  } finally {
    setLoading(false);
  }
});

copyBtn.addEventListener("click", async () => {
  const code = outputEditor.getValue();
  if (!code.trim()) {
    showToast("No hay código para copiar.");
    return;
  }

  try {
    await navigator.clipboard.writeText(code);
    showToast("Código copiado al portapapeles.", "success");
  } catch (error) {
    showToast("No se pudo copiar el código.");
  }
});

fetchHistory();