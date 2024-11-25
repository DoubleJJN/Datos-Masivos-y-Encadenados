from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback

class FlightsScrapper:
    def __init__(self, driver_path, headless=False):
        self.driver_path = driver_path
        self.headless = headless
        self.options = Options()
        self.options.headless = self.headless
        self.service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        #self.driver.get(BASE_URL)

    BASE_URL = "https://flights.booking.com/flights"