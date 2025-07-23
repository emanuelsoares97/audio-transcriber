document.getElementById('uploadForm').onsubmit = async function(e) {
  e.preventDefault();
  const status = document.getElementById('status');
  status.textContent = "A carregar ficheiro...";
  const file = document.getElementById('fileInput').files[0];
  if (!file) return status.textContent = "Selecione um ficheiro.";

  const formData = new FormData();
  formData.append('file', file);

  let resp = await fetch('/api/upload', { method: 'POST', body: formData });
  let data = await resp.json();
  if (!resp.ok) { status.textContent = "Erro: " + data.error; return; }
  status.textContent = "Ficheiro carregado. A processar...";

  // Chama process.js para continuar processamento:
  startProcessing(data.file_path, status);
};
