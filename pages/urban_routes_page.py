from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import Keys


class UrbanRoutesPage:
    """
    Clase de Page Object para Urban Routes.
    Contiene: localizadores (dónde está cada elemento), getters (cómo esperar
    y obtener cada elemento) y métodos de acción/pasos combinados (qué hacer con ellos).
    """

    # ---------- Localizadores: Dirección ----------
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    # ---------- Localizadores: Tarifa ----------
    request_taxi_button = (By.CSS_SELECTOR, '.button.round')
    comfort_tariff = (By.XPATH, '//div[@class="tcard-title" and text()="Comfort"]')
    # Detecta la tarjeta de tarifa que quedó con la clase "active" tras el clic
    comfort_tariff_assert = (By.CSS_SELECTOR, '.tcard.active .tcard-title')

    # ---------- Localizadores: Teléfono ----------
    phone_number_button = (By.CLASS_NAME, 'np-button')
    phone_number_input = (By.ID, 'phone')
    phone_next_button = (By.XPATH, "//button[text()='Siguiente']")
    confirmation_code_input = (By.ID, 'code')
    confirm_code_button = (By.XPATH, "//button[text()='Confirmar']")

    # ---------- Localizadores: Tarjeta de crédito ----------
    payment_method_button = (By.CLASS_NAME, 'pp-button')
    add_card_option = (By.XPATH, "//div[@class='pp-title' and text()='Agregar tarjeta']")
    card_number_input = (By.ID, 'number')
    # Usamos el contenedor .card-code-input porque el id="code" se repite
    # con el campo de código SMS en otro modal (id duplicado en la página).
    card_code_input = (By.CSS_SELECTOR, '.card-code-input input')
    add_card_button = (By.XPATH, "//button[text()='Agregar']")
    card_selected_checkbox = (By.ID, 'card-1')
    close_payment_modal_button = (By.CSS_SELECTOR, '#root > div > div.payment-picker.open > div.modal > div.section.active > button')

    # ---------- Localizadores: Mensaje para el conductor ----------
    message_for_driver_input = (By.ID, 'comment')

    # ---------- Localizadores: Manta y pañuelos ----------
    requirements_section_header = (By.CLASS_NAME, 'reqs-header')
    # Apuntamos al <div class="switch"> visible (el <input> real está oculto por CSS,
    # por eso no es "clickeable" según Selenium aunque exista en el DOM).
    blanket_and_handkerchiefs_switch = (
        By.XPATH,
        "//div[@class='r-sw-label' and text()='Manta y pañuelos']"
        "/following-sibling::div//div[@class='switch']"
    )
    # Este sí apunta al <input> real, para LEER su estado (checked), no para hacer clic.
    blanket_and_handkerchiefs_checkbox = (
        By.XPATH,
        "//div[@class='r-sw-label' and text()='Manta y pañuelos']"
        "/following-sibling::div//input[@class='switch-input']"
    )

    # ---------- Localizadores: Helados ----------
    ice_cream_plus_button = (
        By.XPATH,
        "//div[@class='r-counter-label' and text()='Helado']"
        "/following-sibling::div//div[@class='counter-plus']"
    )
    ice_cream_counter_value = (
        By.XPATH,
        "//div[@class='r-counter-label' and text()='Helado']"
        "/following-sibling::div//div[@class='counter-value']"
    )

    # ---------- Localizadores: Pedir taxi / conductor ----------
    order_taxi_button = (By.CLASS_NAME, 'smart-button')
    search_taxi_modal = (By.CLASS_NAME, 'order-body')
    driver_eta_text = (By.CLASS_NAME, 'order-header-title')

    def __init__(self, driver):
        self.driver = driver
        # Espera explícita estándar (10s), reutilizada por la mayoría de los métodos.
        self.wait = WebDriverWait(driver, 10)

    # ======================== DIRECCIÓN ========================

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
        # Paso combinado: escribe origen y destino en un solo llamado.
        self.set_from(from_address)
        self.set_to(to_address)

    # ======================== TARIFA ========================

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
        # Lee el texto de la tarjeta de tarifa que quedó marcada como "active".
        return self.get_confort_tariff_assert().text

    # ======================== TELÉFONO ========================

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
        # Paso combinado: abre el modal, escribe el número y avanza a "Siguiente".
        # El código de confirmación se maneja aparte en el test (necesita el driver).
        self.click_phone_number_button()
        self.set_phone_number(phone)
        self.click_phone_next_button()

    def get_phone_number(self):
        return self.driver.find_element(*self.phone_number_input).get_property('value')

    # ======================== TARJETA DE CRÉDITO ========================

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
        # Paso combinado: abre el modal de pago, agrega la tarjeta, y la confirma.
        self.click_payment_method_button()
        self.click_add_card_option()
        self.set_card_number(card_number)
        self.set_card_code(card_code)
        # El botón "Agregar" no se activa hasta que el CVV pierda el foco.
        # Simulamos TAB para forzar ese cambio de foco:
        self.driver.find_element(*self.card_code_input).send_keys(Keys.TAB)
        self.click_add_card_button()
        self.driver.save_screenshot('/home/mmt/Documentos/BOOTCAM/qa-project-Urban-Routes-es/debug.png')
        self.click_close_payment_modal_button()

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

    # ======================== MENSAJE PARA EL CONDUCTOR ========================

    def set_message_for_driver(self, message):
        self.wait.until(
            EC.visibility_of_element_located(self.message_for_driver_input)
        ).send_keys(message)

    def get_message_for_driver(self):
        return self.driver.find_element(*self.message_for_driver_input).get_property('value')

    # ======================== MANTA Y PAÑUELOS ========================

    def click_requirements_section_header(self):
        self.wait.until(
            EC.element_to_be_clickable(self.requirements_section_header)
        ).click()

    def click_blanket_and_handkerchiefs_switch(self):
        # Hacemos clic en el <div class="switch"> visible, NO en el <input> oculto.
        self.wait.until(
            EC.element_to_be_clickable(self.blanket_and_handkerchiefs_switch)
        ).click()

    def is_blanket_and_handkerchiefs_selected(self):
        # Leemos el estado directamente del <input>, aunque esté oculto visualmente.
        return self.driver.find_element(
            *self.blanket_and_handkerchiefs_checkbox
        ).get_property('checked')

    # ======================== HELADOS ========================

    def click_ice_cream_plus_button(self):
        self.wait.until(
            EC.element_to_be_clickable(self.ice_cream_plus_button)
        ).click()

    def order_two_ice_creams(self):
        # Paso combinado: pide 2 helados haciendo clic en "+" dos veces.
        self.click_ice_cream_plus_button()
        self.click_ice_cream_plus_button()

    def get_ice_cream_counter(self):
        return self.driver.find_element(*self.ice_cream_counter_value).text

    # ======================== PEDIR TAXI / CONDUCTOR ========================

    def click_order_taxi_button(self):
        self.wait.until(
            EC.element_to_be_clickable(self.order_taxi_button)
        ).click()

    def get_search_taxi_modal(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.search_taxi_modal)
        )

    def wait_for_driver_info(self):
        # Espera más larga (60s): el modal tarda en pasar de "Buscar automóvil"
        # a mostrar la información real del conductor asignado.
        long_wait = WebDriverWait(self.driver, 60)
        long_wait.until(
            EC.text_to_be_present_in_element(self.driver_eta_text, "llegará en")
        )
        return self.driver.find_element(*self.driver_eta_text)