from data import data
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from pages.urban_routes_page import UrbanRoutesPage
from utils.retrive_code import retrieve_phone_code


class TestUrbanRoutes:

    driver = None

    def setup_method(self):
        options = Options()
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        self.driver = webdriver.Chrome(service=Service(), options=options)
        self.driver.get(data.urban_routes_url)
        self.routes_page = UrbanRoutesPage(self.driver)

    def test_1_set_route(self):
        address_from = data.address_from
        address_to = data.address_to
        self.routes_page.set_route(address_from, address_to)
        assert self.routes_page.get_from() == address_from
        assert self.routes_page.get_to() == address_to

    def test_2_select_comfort_tariff(self):
        address_from = data.address_from
        address_to = data.address_to
        self.routes_page.set_route(address_from, address_to)
        self.routes_page.click_request_taxi_button()
        self.routes_page.click_comfort_tariff()
        assert self.routes_page.reader_confort_tariff_assert() == "Comfort"

    def test_3_fill_phone_number(self):
        address_from = data.address_from
        address_to = data.address_to
        phone_number = data.phone_number
        self.routes_page.set_route(address_from, address_to)
        self.routes_page.click_request_taxi_button()
        self.routes_page.click_comfort_tariff()
        self.routes_page.fill_phone_number(phone_number)
        code = retrieve_phone_code(self.driver)
        self.routes_page.set_confirmation_code(code)
        self.routes_page.click_confirm_code_button()
        assert self.routes_page.get_phone_number() == phone_number

    def test_4_fill_card(self):
        address_from = data.address_from
        address_to = data.address_to
        card_number = data.card_number
        card_code = data.card_code
        self.routes_page.set_route(address_from, address_to)
        self.routes_page.click_request_taxi_button()
        self.routes_page.click_comfort_tariff()
        self.routes_page.fill_card(card_number, card_code)
        assert self.routes_page.is_card_selected() is True


    def teardown_method(self):
        # Se ejecuta DESPUÉS de cada test: cierra el navegador.
        self.driver.quit()