from data import data
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from pages.urban_routes_page import UrbanRoutesPage
from utils.retrive_code import retrieve_phone_code


class TestUrbanRoutes:
    """
    Suite de pruebas de Urban Routes.
    Cada test es independiente: setup_method abre un navegador limpio antes
    de cada uno, y teardown_method lo cierra al terminar.
    """

    driver = None

    def setup_method(self):
        # Habilita el registro de red (necesario para retrieve_phone_code)
        # y abre un navegador nuevo antes de cada test.
        options = Options()
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        self.driver = webdriver.Chrome(service=Service(), options=options)
        self.driver.get(data.urban_routes_url)
        self.routes_page = UrbanRoutesPage(self.driver)

    # ---------- 1. Configurar dirección ----------
    def test_1_set_route(self):
        address_from = data.address_from
        address_to = data.address_to
        self.routes_page.set_route(address_from, address_to)
        assert self.routes_page.get_from() == address_from
        assert self.routes_page.get_to() == address_to

    # ---------- 2. Seleccionar tarifa Comfort ----------
    def test_2_select_comfort_tariff(self):
        address_from = data.address_from
        address_to = data.address_to
        self.routes_page.set_route(address_from, address_to)
        self.routes_page.click_request_taxi_button()
        self.routes_page.click_comfort_tariff()
        assert self.routes_page.reader_confort_tariff_assert() == "Comfort"

    # ---------- 3. Rellenar teléfono ----------
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

    # ---------- 4. Agregar tarjeta de crédito ----------
    def test_4_fill_card(self):
        address_from = data.address_from
        address_to = data.address_to
        card_number = data.card_number
        card_code = data.card_code
        self.routes_page.set_route(address_from, address_to)
        self.routes_page.click_request_taxi_button()
        self.routes_page.click_comfort_tariff()
        self.routes_page.fill_card(card_number, card_code)
        assert self.routes_page.is_card_selected()

    # ---------- 5. Escribir mensaje para el conductor ----------
    def test_5_set_message_for_driver(self):
        address_from = data.address_from
        address_to = data.address_to
        message = data.message_for_driver
        self.routes_page.set_route(address_from, address_to)
        self.routes_page.click_request_taxi_button()
        self.routes_page.click_comfort_tariff()
        self.routes_page.set_message_for_driver(message)
        assert self.routes_page.get_message_for_driver() == message

    # ---------- 6. Pedir manta y pañuelos ----------
    def test_6_order_blanket_and_handkerchiefs(self):
        address_from = data.address_from
        address_to = data.address_to
        self.routes_page.set_route(address_from, address_to)
        self.routes_page.click_request_taxi_button()
        self.routes_page.click_comfort_tariff()
        self.routes_page.click_blanket_and_handkerchiefs_switch()
        assert self.routes_page.is_blanket_and_handkerchiefs_selected()

    # ---------- 7. Pedir 2 helados ----------
    def test_7_order_two_ice_creams(self):
        address_from = data.address_from
        address_to = data.address_to
        self.routes_page.set_route(address_from, address_to)
        self.routes_page.click_request_taxi_button()
        self.routes_page.click_comfort_tariff()
        self.routes_page.order_two_ice_creams()
        assert self.routes_page.get_ice_cream_counter() == "2"

    # ---------- 8. Pedir el taxi (modal de búsqueda) ----------
    # Necesita el flujo COMPLETO: la app no permite pedir el taxi
    # sin teléfono confirmado y tarjeta agregada.
    def test_8_order_taxi(self):
        address_from = data.address_from
        address_to = data.address_to
        phone_number = data.phone_number
        card_number = data.card_number
        card_code = data.card_code
        message = data.message_for_driver

        self.routes_page.set_route(address_from, address_to)
        self.routes_page.click_request_taxi_button()
        self.routes_page.click_comfort_tariff()
        self.routes_page.fill_phone_number(phone_number)
        code = retrieve_phone_code(self.driver)
        self.routes_page.set_confirmation_code(code)
        self.routes_page.click_confirm_code_button()
        self.routes_page.fill_card(card_number, card_code)
        self.routes_page.set_message_for_driver(message)
        self.routes_page.click_order_taxi_button()

        assert self.routes_page.get_search_taxi_modal().is_displayed()

    # ---------- 9. (Opcional) Esperar info del conductor asignado ----------
    # Mismo flujo completo que el test 8, porque sin teléfono/tarjeta
    # nunca se asigna un conductor real (el modal se queda "buscando").
    def test_9_wait_for_driver_info(self):
        address_from = data.address_from
        address_to = data.address_to
        phone_number = data.phone_number
        card_number = data.card_number
        card_code = data.card_code
        message = data.message_for_driver

        self.routes_page.set_route(address_from, address_to)
        self.routes_page.click_request_taxi_button()
        self.routes_page.click_comfort_tariff()
        self.routes_page.fill_phone_number(phone_number)
        code = retrieve_phone_code(self.driver)
        self.routes_page.set_confirmation_code(code)
        self.routes_page.click_confirm_code_button()
        self.routes_page.fill_card(card_number, card_code)
        self.routes_page.set_message_for_driver(message)
        self.routes_page.click_order_taxi_button()

        driver_info = self.routes_page.wait_for_driver_info()
        assert "llegará en" in driver_info.text.lower()

    def teardown_method(self):
        # Se ejecuta DESPUÉS de cada test: cierra el navegador.
        self.driver.quit()