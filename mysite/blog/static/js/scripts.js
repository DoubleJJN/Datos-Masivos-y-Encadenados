function showLoader(id) {
    document.getElementById(id).style.display = 'block';
}

function hideLoader(id) {
    document.getElementById(id).style.display = 'none';
}

function fetchOllamaQuery() {
    showLoader("loader_ollama");

    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get('q');  // Valor predeterminado
    fetch(`api/ollama_query/?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            hideLoader("loader_ollama");
            const resultContainer = document.querySelector('#result_ollama');
            if (data.error) {
                resultContainer.innerHTML = `<p class="error">${data.error}</p>`;
            } else {
                resultContainer.textContent = data.result;
            }
        })
        .catch(error => {
            hideLoader("loader_ollama");
            console.error('Error al obtener la consulta:', error);
            document.querySelector('#result_ollama').innerHTML = `<p class="error">Error al obtener la consulta</p>`;
        });
}

function get_flights() {
    showLoader("loader_flights");

    const urlParams = new URLSearchParams(window.location.search);
    const departure = "Madrid";  // Valor predeterminado
    const query = urlParams.get('q');
    const departure_date = urlParams.get('departure_date');
    const return_date = urlParams.get('return_date');
    const num_people = urlParams.get('num_people');

    fetch(`api/get_flights/?departure=${departure}&q=${query}&departure_date=${departure_date}&return_date=${return_date}&num_people=${num_people}`)
        .then(response => response.json())
        .then(data => {
            hideLoader("loader_flights");
            const resultContainer = document.querySelector('#result_flights');
            resultContainer.innerHTML = ''; // Limpia los resultados previos

            if (data.error) {
                resultContainer.innerHTML = `<p class="error">${data.error}</p>`;
            } else if (data.flights.length > 0) {
                data.flights.forEach(flight => {
                    const flightHTML = `
                        <div class="col">
                            <div class="card shadow-sm d-flex flex-row align-items-center">
                                <div class="card-body d-flex flex-grow-1 justify-content-between align-items-center">
                                    <div class="details" style="flex: 1;">

                                        <h6 class="card-title mb-2">Ida</h6>
                                        <p><strong>Salida:</strong> ${flight.vuelo_ida.hora_salida} - <strong>Llegada:</strong> ${flight.vuelo_ida.hora_llegada}</p>
                                        <p><strong>Duración:</strong> ${flight.vuelo_ida.duracion}</p>

                                        <h6 class="card-title mb-2">Vuelta</h6>
                                        <p><strong>Salida:</strong> ${flight.vuelo_vuelta.hora_salida} - <strong>Llegada:</strong> ${flight.vuelo_vuelta.hora_llegada}</p>
                                        <p><strong>Duración:</strong> ${flight.vuelo_vuelta.duracion}</p>


                                    </div>
                                  
                                    <div class="details-price" style="flex: 1;">
                                        <p><strong>Precio:</strong> ${flight.precio_individual} por persona</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                    resultContainer.insertAdjacentHTML('beforeend', flightHTML);
                });
            } else {
                resultContainer.innerHTML = `
                    <div class="col">
                        <p>No hay vuelos disponibles hacia este destino.</p>
                    </div>
                `;
            }
        })
        .catch(error => {
            hideLoader("loader_flights");
            console.error('Error al obtener los vuelos:', error);
            document.querySelector('#result_flights').innerHTML = `
                <div class="col">
                    <p class="error">Error al obtener los vuelos. Inténtalo de nuevo.</p>
                </div>
            `;
        });
}

document.addEventListener("DOMContentLoaded", function() {
    fetchOllamaQuery();
    get_flights();
});