async function startProcessing(file_path, status) {
  let resp = await fetch('/api/process', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ file_path: file_path, num_speakers: 2, language: "pt" })
  });
  let data = await resp.json();
  if (!resp.ok) { status.textContent = "Erro: " + data.error; return; }
  status.textContent = "Processamento concluído!";
  
  // Mostra resultado na página
  const resultDiv = document.getElementById('result');
  let html = "<b>Transcrição por locutor:</b><ul>";
  for(let seg of data.segments){
    html += `<li><b>${seg.speaker}</b> [${seg.start.toFixed(2)}s-${seg.end.toFixed(2)}s]: ${seg.text}</li>`;
  }
  html += "</ul>";
  if(data.output_json){
    html += `<a href="${data.output_json}" download>Download JSON</a>`;
  }
  resultDiv.innerHTML = html;
}
