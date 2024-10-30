import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def configure_driver():
    """
    Configura el controlador de Selenium en modo headless para realizar la extracción sin abrir una ventana gráfica.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver_path = "/usr/local/bin/chromedriver"
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    return driver

def gather_google_maps_data(driver, business_type, location):
    """
    Abre Google Maps con el tipo de negocio y la ubicación especificados, desplaza la página hasta el final y hace clic en
    cada negocio para obtener información adicional.
    Guarda la página HTML en el directorio `data` para procesamiento posterior.
    """
    # Construir la URL de búsqueda
    search_url = f"https://www.google.com/maps/search/{business_type}+en+{location}"
    driver.get(search_url)

    # Esperar que se carguen los resultados
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'section-result-content'))
    )

    # Desplazarse hacia abajo para cargar todos los resultados
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_attempts = 0
    while scroll_attempts < 5:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            scroll_attempts += 1
        else:
            last_height = new_height
            scroll_attempts = 0

    # Hacer clic en cada negocio para cargar detalles
    business_listings = driver.find_elements(By.CLASS_NAME, 'section-result-content')
    for business in business_listings:
        try:
            business.click()
            time.sleep(2)
        except Exception as e:
            print("Error al hacer clic en el negocio:", e)
            continue

    # Guardar el HTML en el directorio `data`
    page_html = driver.page_source
    with open("data/google_maps_results.html", "w", encoding="utf-8") as file:
        file.write(page_html)
    print("HTML de resultados guardado en data/google_maps_results.html")

def main():
    # Solicitar datos al usuario
    business_type = input("Ingrese el tipo de negocio a buscar: ")
    location = input("Ingrese la ubicación o ciudad: ")

    # Ejecutar el navegador y recopilar datos
    driver = configure_driver()
    gather_google_maps_data(driver, business_type, location)
    driver.quit()

if __name__ == "__main__":
    main()
