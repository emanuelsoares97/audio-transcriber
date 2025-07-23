document.getElementById('upload-form').onsubmit = async function(e) {
    e.preventDefault();
    const form = e.target;
    const file = form['audio-file'].files[0];
    if (!file) return;
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '<div class="text-center text-info">Processando, aguarde...</div>';
    const data = new FormData();
    data.append('file', file);
    let resp = await fetch('/api/upload', {method: 'POST', body: data});
    let json = await resp.json();
    if (json.error) {
        resultDiv.innerHTML = `<div class="alert alert-danger">${json.error}</div>`;
        return;
    }
    resultDiv.innerHTML = `<div class="alert alert-success">Upload realizado com sucesso! A processar...</div>`;

     if (json.file_path) {
        startProcessing(json.file_path, resultDiv);
    } else {
        resultDiv.innerHTML += `<div class="alert alert-warning">Ficheiro não processável!</div>`;

    }

};
