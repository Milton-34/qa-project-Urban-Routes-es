# QA Project: Urban Routes (ES)

## Descripción del proyecto

Este proyecto contiene un conjunto de pruebas automatizadas de interfaz de usuario (UI) para **Urban Routes**, una aplicación web de pedido de taxis. Las pruebas cubren el flujo completo de un usuario al solicitar un viaje: configuración de la ruta, selección de tarifa, registro de teléfono, método de pago, mensaje al conductor, requisitos adicionales del pedido y la solicitud final del taxi (incluyendo la espera de asignación de un conductor).

El proyecto sigue el patrón de diseño **Page Object Model (POM)**, separando la lógica de interacción con la interfaz (localizadores y métodos de la página) de la lógica de las pruebas en sí, siguiendo buenas prácticas de automatización de QA.

## Tecnologías y técnicas utilizadas

- **Python 3** — lenguaje de programación del proyecto.
- **Selenium WebDriver** — automatización del navegador (Google Chrome).
- **pytest** — framework de ejecución y organización de pruebas.
- **Page Object Model (POM)** — patrón de diseño que separa la representación de la página (localizadores, getters y métodos de acción) de las pruebas.
- **Combinación de métodos en pasos** — los métodos atómicos (clics, escritura de texto) se combinan en métodos de más alto nivel que representan una acción completa del usuario (ej. `fill_card`, `fill_phone_number`, `set_route`).
- **Esperas explícitas (`WebDriverWait` + `expected_conditions`)** — en lugar de esperas fijas (`time.sleep`), se usan condiciones que esperan a que un elemento esté presente, visible o sea clickeable, haciendo las pruebas más robustas frente a la carga asíncrona de la página.
- **Localizadores CSS y XPath** — incluyendo selectores anclados a contenedores específicos para resolver ambigüedades cuando varios elementos comparten la misma clase (por ejemplo, distinguir el botón de cerrar del modal de teléfono del de tarjeta).
- **Interceptación de peticiones de red** — la función `retrieve_phone_code` utiliza los logs de rendimiento del navegador (`performance logs`) para obtener el código de confirmación del teléfono, sin depender de un SMS real.
- **Independencia de pruebas** (`setup_method` / `teardown_method`) — cada prueba se ejecuta en una instancia de navegador nueva y limpia, evitando que el estado de una prueba afecte a otra.

## Estructura del proyecto

```
qa-project-Urban-Routes-es/
├── data/
│   ├── __init__.py
│   └── data.py                  # URL del servidor y datos de prueba (direcciones, teléfono, tarjeta, etc.)
├── pages/
│   ├── __init__.py
│   └── urban_routes_page.py     # Clase UrbanRoutesPage (localizadores, getters, métodos de acción)
├── utils/
│   ├── __init__.py
│   └── retrive_code.py          # Función retrieve_phone_code (no modificar)
├── test/
│   └── test_uban_routes.py      # Casos de prueba (clase TestUrbanRoutes)
└── README.md
```

## Casos de prueba cubiertos

1. **Configurar la dirección** de origen y destino.
2. **Seleccionar la tarifa Comfort**.
3. **Rellenar el número de teléfono** y confirmarlo con el código de SMS interceptado.
4. **Agregar una tarjeta de crédito**, incluyendo el manejo del campo CVV (simulando `TAB` para activar el botón de guardado).
5. **Escribir un mensaje** para el conductor.
6. **Pedir manta y pañuelos**.
7. **Pedir 2 helados**.
8. **Solicitar el taxi**, verificando que aparece el modal de búsqueda.
9. **(Opcional) Esperar la asignación del conductor**, verificando que el modal cambia de "buscando" a mostrar la información real del viaje.

## Cómo ejecutar las pruebas

### Requisitos previos

- Python 3 instalado.
- Google Chrome instalado.
- Dependencias del proyecto instaladas (Selenium, pytest):

```bash
pip install selenium pytest
```

### Configuración

En `data/data.py`, asegúrate de que `urban_routes_url` apunte a la URL del servidor de Urban Routes generada para tu sesión.

### Ejecutar todas las pruebas

Desde la raíz del proyecto:

```bash
pytest test/test_uban_routes.py -v
```

### Ejecutar una prueba específica

```bash
pytest test/test_uban_routes.py::TestUrbanRoutes::test_1_set_route -v
```

### Notas

- Cada prueba abre y cierra su propia instancia de navegador, por lo que pueden ejecutarse de forma independiente o en conjunto.
- La prueba `test_9_wait_for_driver_info` puede tardar más tiempo en completarse (hasta 60 segundos), ya que espera a que el sistema simule la asignación de un conductor.
