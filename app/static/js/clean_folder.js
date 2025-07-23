document.getElementById('btn-limpar').onclick = async function() {
    const statusDiv = document.getElementById('limpar-status');
    statusDiv.textContent = 'A limpar...';
    let resp = await fetch('/clean', {method: 'POST'});
    if (!resp.ok) {
        statusDiv.textContent = 'Erro ao limpar.';
        return;
    }
    let data = await resp.json();
    statusDiv.textContent = data.mensagem || 'Limpeza feita!';

    setTimeout(() => {
        statusDiv.textContent = '';
    }, 3000);
};
