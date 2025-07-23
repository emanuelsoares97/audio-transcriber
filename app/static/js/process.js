async function startProcessing(file_path, status) {
    let resp = await fetch('/api/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_path: file_path, num_speakers: 2, language: "pt" })
    });
    let data = await resp.json();
    if (!resp.ok) { status.textContent = "Erro: " + data.error; return; }
    status.textContent = "Processamento concluído!";

    const resultDiv = document.getElementById('result');
    let html = "<b>Transcrição por locutor:</b><ul>";
    for (let seg of data.segments || []) {
        html += `<li><b>${seg.speaker}</b> [${seg.start.toFixed(2)}s-${seg.end.toFixed(2)}s]: ${seg.text}</li>`;
    }
    html += "</ul>";

    // Botão JSON
    if (data.output_json) {
        html += `<a href="${data.output_json}" class="btn btn-outline-primary mt-3" download>Download Transcrição (JSON)</a>`;
    }
    // Botão Exportar PDF
    if (data.segments) {
        html += `<button class="btn btn-primary mt-3" id="btn-pdf">Exportar em PDF</button>`;
    }

    resultDiv.innerHTML = html;

    
    if (data.segments) {
        document.getElementById("btn-pdf").onclick = async () => {
            let resp = await fetch("/api/export/pdf", {
                method: "POST",
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ segments: data.segments })
            });
            let pdfData = await resp.json();
            if (pdfData.pdf_url) {
                resultDiv.innerHTML += `<a href="${pdfData.pdf_url}" class="btn btn-outline-primary mt-3" download>Descarregar PDF</a>`;
            } else {
                resultDiv.innerHTML += "<div class='text-danger'>Erro ao gerar PDF!</div>";
            }
        }
    }
}
