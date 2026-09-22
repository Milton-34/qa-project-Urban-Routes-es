from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import Keys


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    request_taxi_button = (By.CSS_SELECTOR, '.button.round')
    comfort_tariff = (By.XPATH, '//div[@class="tcard-title" and text()="Comfort"]')
    comfort_tariff_assert = (By.CSS_SELECTOR, '.tcard.active .tcard-title')
    phone_number_button = (By.CLASS_NAME, 'np-button')
    phone_number_input = (By.ID, 'phone')
    phone_next_button = (By.XPATH, "//button[text()='Siguiente']")
    confirmation_code_input = (By.ID, 'code')
    confirm_code_button = (By.XPATH, "//button[text()='Confirmar']")
    payment_method_button = (By.CLASS_NAME, 'pp-button')
    add_card_option = (By.XPATH, "//div[@class='pp-title' and text()='Agregar tarjeta']")
    card_number_input = (By.ID, 'number')
    card_code_input = (By.CSS_SELECTOR, '.card-code-input input')
    add_card_button = (By.XPATH, "//button[text()='Agregar']")
    card_selected_checkbox = (By.ID, 'card-1')
    close_payment_modal_button = (By.CLASS_NAME, 'close-button')


    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def set_from(self, from_address):
        self.wait.until(
            EC.presence_of_element_located(self.from_field)
        ).send_keys(from_address)

    def set_to(self, to_address):
        self.wait.until(
            EC.presence_of_element_located(self.to_field)
        ).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, from_address, to_address):
        # Paso combinado (patrón visto en "Combinación de métodos en pasos")
        self.set_from(from_address)
        self.set_to(to_address)

    def get_request_taxi_button(self):
        return self.wait.until(
            EC.element_to_be_clickable(self.request_taxi_button)
        )

    def click_request_taxi_button(self):
        self.get_request_taxi_button().click()

    def get_comfort_tariff(self):
        return self.wait.until(
            EC.element_to_be_clickable(self.comfort_tariff)
        )
    def click_comfort_tariff(self):
        self.get_comfort_tariff().click()

    def get_confort_tariff_assert(self):
        return self.wait.until(
            EC.presence_of_element_located(self.comfort_tariff_assert)
        )

    def reader_confort_tariff_assert(self):
        confort_tariff = self.get_confort_tariff_assert().text
        return confort_tariff

    # ---------- Teléfono ----------
    def click_phone_number_button(self):
        self.wait.until(
            EC.element_to_be_clickable(self.phone_number_button)
        ).click()

    def set_phone_number(self, phone):
        self.wait.until(
            EC.visibility_of_element_located(self.phone_number_input)
        ).send_keys(phone)

    def click_phone_next_button(self):
        self.wait.until(
            EC.element_to_be_clickable(self.phone_next_button)
        ).click()

    def set_confirmation_code(self, code):
        self.wait.until(
            EC.visibility_of_element_located(self.confirmation_code_input)
        ).send_keys(code)

    def click_confirm_code_button(self):
        self.wait.until(
            EC.element_to_be_clickable(self.confirm_code_button)
        ).click()

    def fill_phone_number(self, phone):
        # Paso combinado: todo el flujo de teléfono en un solo método
        self.click_phone_number_button()
        self.set_phone_number(phone)
        self.click_phone_next_button()

    def get_phone_number(self):
        return self.driver.find_element(*self.phone_number_input).get_property('value')

    def click_payment_method_button(self):
        self.wait.until(
            EC.element_to_be_clickable(self.payment_method_button)
        ).click()

    def click_add_card_option(self):
        self.wait.until(
            EC.element_to_be_clickable(self.add_card_option)
        ).click()

    def set_card_number(self, number):
        self.wait.until(
            EC.visibility_of_element_located(self.card_number_input)
        ).send_keys(number)

    def set_card_code(self, code):
        self.wait.until(
            EC.visibility_of_element_located(self.card_code_input)
        ).send_keys(code)

    def click_add_card_button(self):
        self.wait.until(
            EC.element_to_be_clickable(self.add_card_button)
        ).click()

    def fill_card(self, card_number, card_code):
        self.click_payment_method_button()
        self.click_add_card_option()
        self.set_card_number(card_number)
        self.set_card_code(card_code)
        # El botón "Agregar" no se activa hasta que el CVV pierda el foco.
        # Simulamos TAB para que el campo pierda el enfoque:
        self.driver.find_element(*self.card_code_input).send_keys(Keys.TAB)
        self.click_add_card_button()

    def get_card_selected_checkbox(self):
        return self.wait.until(
            EC.presence_of_element_located(self.card_selected_checkbox)
        )

    def is_card_selected(self):
        return self.get_card_selected_checkbox().get_property('checked')

    def click_close_payment_modal_button(self):
        self.wait.until(
            EC.element_to_be_clickable(self.close_payment_modal_button)
        ).click()

