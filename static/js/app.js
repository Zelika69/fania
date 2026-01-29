const translateBtn = document.getElementById("translateBtn");
const loader = document.getElementById("loader");
const toastEl = document.getElementById("appToast");
const toastBody = document.getElementById("toastBody");
const copyBtn = document.getElementById("copyBtn");
const explanationBox = document.getElementById("explanation");

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