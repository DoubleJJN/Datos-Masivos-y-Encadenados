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
    const query = correctedPlace;
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
                            <div class="data-card shadow-sm d-flex flex-row align-items-center">
                                <div class="card-body d-flex flex-grow-1 justify-content-between align-items-center">
                                    <div class="details" style="flex: 1; display: flex; flex-direction: row; gap: 10px;">
                                        <div>
                                            <h5 class="card-title mb-2 custom-color"><strong>Ida</strong></h5>
                                            <div>
                                                <p><strong>Salida:</strong> ${flight.vuelo_ida.hora_salida} - <strong>Llegada:</strong> ${flight.vuelo_ida.hora_llegada}</p>
                                                <p><strong>Duración:</strong> ${flight.vuelo_ida.duracion}</p>
                                            </div>
                                        </div>
                                        <div>
                                            <h5 class="card-title mb-2 custom-color"><strong>Vuelta</strong></h5>
                                            <div>
                                                <p><strong>Salida:</strong> ${flight.vuelo_vuelta.hora_salida} - <strong>Llegada:</strong> ${flight.vuelo_vuelta.hora_llegada}</p>
                                                <p><strong>Duración:</strong> ${flight.vuelo_vuelta.duracion}</p>
                                            </div>
                                        </div>
                                        
                                        <div class="details-price" style="flex: 1; text-align: right;">
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
function fixEncoding(text) {
    return new TextDecoder("utf-8").decode(new TextEncoder().encode(text));
}
function get_hotels() {
    showLoader("loader_hotels");
    //load commodities.txt and hotels.txt
    fetch(`api/get_hotels/`)
        .then(response => response.json())
        .then(data => {
            hideLoader("loader_hotels");
            const resultContainer = document.querySelector('#result_hotels');
            resultContainer.innerHTML = ''; // Limpia los resultados previos
            console.log(data);
            if (data.error) {
                resultContainer.innerHTML = `<p class="error">${data.error}</p>`;
            } else if (data.hotels.length > 0) {
                data.hotels.forEach(hotel => {
                    const hotelHTML = `
                        <div class="col">
                            <div class="data-card shadow-sm" style="border-radius: 10px; overflow: hidden;">
                                <div class="card-header d-flex justify-content-between" style="background-color: var(--primary-color); color: white;">
                                    <h5 class="mb-0"><strong>${hotel.HotelName}</strong></h5>
                                    <span class="badge bg-light text-dark">${hotel.Rating} ★</span>
                                </div>
                                <div class="card-body d-flex flex-column">
                                    <div class="details d-flex flex-column gap-3">
                                        <div>
                                            <p class="mb-1"><strong>Precio por noche:</strong> <span class="text-success">$${hotel.PricePerNight}</span></p>
                                        </div>
                                        <div>
                                            <p class="mb-1"><strong>Comodidades:</strong></p>
                                            <ul class="ps-3 mb-0">
                                                ${hotel.Commodities.map(commodity => `<li>${fixEncoding(commodity)}</li>`).join('')}
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                                <div class="card-footer d-flex justify-content-end" style="background-color: var(--secondary-color);">
                                    <a href="www.trivago.es"><button class="btn btn-primary">Reservar</button></a>
                                </div>
                            </div>
                        </div>
                    `;
                    resultContainer.insertAdjacentHTML('beforeend', hotelHTML);
                });
            } else {
                resultContainer.innerHTML = `
                    <div class="col">
                        <p>No hay hoteles disponibles en este destino.</p>
                    </div>
                `;
            }
        })
        .catch(error => {
            hideLoader("loader_hotels");
            console.error('Error al obtener los hoteles:', error);
            document.querySelector('#loader_hotels').innerHTML = `
                <div class="col">
                    <p class="error">Error al obtener los hoteles. Inténtalo de nuevo.</p>
                </div>
            `;
        });
}

document.addEventListener("DOMContentLoaded", function () {
    const correctedPlace = window.correctedPlace || null;
    fetchOllamaQuery();
    get_flights();
    get_hotels();
});