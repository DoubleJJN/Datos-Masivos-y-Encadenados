from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import traceback

class FlightsScrapper:
    def __init__(self):
        self.base_url = "https://flights.booking.com/flights"
        self.headless = True
        self.options = Options()
        if self.headless:
            self.options.add_argument("--headless")
            self.options.add_argument("--disable-gpu")
            self.options.add_argument("--no-sandbox")
            self.options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

    def url_builder(self, departure, arrival, num_people, aeropuerto_origen, aeropuerto_destino, fecha_ida, fecha_vuelta):
        return f"{self.base_url}/{departure}.AIRPORT-{arrival}.AIRPORT/?type=ROUNDTRIP&adults={num_people}&cabinClass=ECONOMY&children=&from={departure}.AIRPORT&to={arrival}.AIRPORT&fromCountry=ES&toCountry=IT&fromLocationName={aeropuerto_origen}&toLocationName={aeropuerto_destino}&depart={fecha_ida}&return={fecha_vuelta}&sort=BEST"
    


    # iniciar la busqueda
    def scrape(self, departure, arrival, departure_date, arrival_date, num_people):
        # Iniciar el navegador
        url = self.url_builder("MAD", "FCO", "2", "Aeropuerto+Adolfo+Suárez+Madrid+-+Barajas", "Aeropuerto+de+Roma+-+Fiumicino", "2024-12-21", "2024-12-28")
        self.driver.get(url)

        # Esperar a que la página cargue
        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.presence_of_element_located((By.XPATH, "//ul[contains(@class, 'List-module__root')]")))

        try:
            # Extraer la información
            flights_data = []

            # Seleccionar todos los elementos <li> dentro del <ul>
            flights = self.driver.find_elements(By.XPATH, "//ul[contains(@class, 'List-module__root')]//li[contains(@class, 'List-module__item')]")

            for flight in flights:
                try:
                    flight_info = self.get_data(flight)
                    flights_data.append(flight_info)

                except Exception as e:
                    print(f"Error extrayendo datos de un vuelo: {e}")
                    
        except Exception as e:
            print("Ocurrió un error:")
            traceback.print_exc()

        finally:
            self.driver.quit()

        return flights_data
    
    def get_data(self, flight):
        # Fechas y horas de salida/llegada (ida y vuelta)
            vuelo_ida_hora_salida = flight.find_element(By.XPATH, ".//*[contains(@data-testid, 'flight_card_segment_departure_time_0')]").text
            vuelo_ida_lugar = flight.find_element(By.XPATH, ".//*[contains(@data-testid, 'flight_card_segment_departure_airport_0')]").text
            vuelo_ida_fecha = flight.find_element(By.XPATH, ".//*[contains(@data-testid, 'flight_card_segment_departure_date_0')]").text
            vuelo_ida_duracion = flight.find_element(By.XPATH, ".//*[contains(@data-testid, 'flight_card_segment_duration_0')]").text
            vuelo_ida_hora_llegada = flight.find_element(By.XPATH, ".//*[contains(@data-testid, 'flight_card_segment_destination_time_0')]").text
            vuelo_ida_lugar_llegada = flight.find_element(By.XPATH, ".//*[contains(@data-testid, 'flight_card_segment_destination_airport_0')]").text
            vuelo_ida_fecha_llegada = flight.find_element(By.XPATH, ".//*[contains(@data-testid, 'flight_card_segment_destination_date_0')]").text
            vuelo_vuelta_hora_salida = flight.find_element(By.XPATH, ".//*[contains(@data-testid, 'flight_card_segment_departure_time_1')]").text
            vuelo_vuelta_lugar = flight.find_element(By.XPATH, ".//*[contains(@data-testid, 'flight_card_segment_departure_airport_1')]").text
            vuelo_vuelta_fecha = flight.find_element(By.XPATH, ".//*[contains(@data-testid, 'flight_card_segment_departure_date_1')]").text
            vuelo_vuelta_duracion = flight.find_element(By.XPATH, ".//*[contains(@data-testid, 'flight_card_segment_duration_1')]").text
            vuelo_vuelta_hora_llegada = flight.find_element(By.XPATH, ".//*[contains(@data-testid, 'flight_card_segment_destination_time_1')]").text
            vuelo_vuelta_lugar_llegada = flight.find_element(By.XPATH, ".//*[contains(@data-testid, 'flight_card_segment_destination_airport_1')]").text
            vuelo_vuelta_fecha_llegada = flight.find_element(By.XPATH, ".//*[contains(@data-testid, 'flight_card_segment_destination_date_1')]").text
                    
            # Precios
            precio_individual = flight.find_element(By.XPATH, ".//*[contains(@data-testid, 'flight_card_price_main_price')]").text
            precio_total = flight.find_element(By.XPATH, ".//*[contains(@data-testid, 'flight_card_price_total_price')]").text
            
            # Aerolínea

            # Almacenar los datos en un diccionario
            flight_info = {
                "precio_individual": precio_individual,
                "precio_total": precio_total,
                "vuelo_ida": {
                    "hora_salida": vuelo_ida_hora_salida,
                    "lugar_salida": vuelo_ida_lugar,
                    "fecha_salida": vuelo_ida_fecha,
                    "duracion": vuelo_ida_duracion,
                    "hora_llegada": vuelo_ida_hora_llegada,
                    "lugar_llegada": vuelo_ida_lugar_llegada,
                    "fecha_llegada": vuelo_ida_fecha_llegada
                },
                "vuelo_vuelta": {
                    "hora_salida": vuelo_vuelta_hora_salida,
                    "lugar_salida": vuelo_vuelta_lugar,
                    "fecha_salida": vuelo_vuelta_fecha,
                    "duracion": vuelo_vuelta_duracion,
                    "hora_llegada": vuelo_vuelta_hora_llegada,
                    "lugar_llegada": vuelo_vuelta_lugar_llegada,
                    "fecha_llegada": vuelo_vuelta_fecha_llegada
                }
            }
                    
            return flight_info
    
    def get_first_flight(self, departure, arrival, departure_date, arrival_date, num_people):
        flight = self.scrape(departure, arrival, departure_date, arrival_date, num_people)[0]
        return flight
    
# ejemplo de uso
if __name__ == "__main__":
    scrapper = FlightsScrapper()
    #data = scrapper.scrape('MAD', 'FCO', '2024-12-21', '2024-12-28', '2')
    data = scrapper.get_first_flight('MAD', 'FCO', '2024-12-21', '2024-12-28', '2')
    print(data)