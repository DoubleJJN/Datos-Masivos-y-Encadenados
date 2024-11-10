function showLoader() {
    document.getElementById('loader').style.display = 'block';
}

function hideLoader() {
    document.getElementById('loader').style.display = 'none';
}

function fetchOllamaQuery() {
    showLoader();

    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get('q');  // Valor predeterminado
    fetch(`api/ollama_query/?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            hideLoader();
            const resultContainer = document.querySelector('.result');
            if (data.error) {
                resultContainer.innerHTML = `<p class="error">${data.error}</p>`;
            } else {
                resultContainer.textContent = data.result;
            }
        })
        .catch(error => {
            hideLoader();
            console.error('Error al obtener la consulta:', error);
            document.querySelector('.result').innerHTML = `<p class="error">Error al obtener la consulta</p>`;
        });
}

document.addEventListener("DOMContentLoaded", function() {
    fetchOllamaQuery();
});