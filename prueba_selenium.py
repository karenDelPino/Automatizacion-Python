import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

print("Iniciando navegador...")

# 2. CONFIGURAR CHROME PARA QUE NO MOLESTE
opciones = Options()
opciones.add_experimental_option("prefs", {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False
})
opciones.add_argument("--disable-notifications") # Evita otros carteles molestos

# 3. INICIAR EL DRIVER CON ESTAS OPCIONES
driver = webdriver.Chrome(options=opciones)
wait = WebDriverWait(driver, 10)

try:
    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()
    time.sleep(1) # Pausa inicial

    # Login
    print("Iniciando sesión...")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    time.sleep(0.5)
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    time.sleep(0.5)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(1.5) # Pausa para ver el catálogo

    # Carrito
    print("Agregando producto al carrito...")
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    time.sleep(1)
    
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    time.sleep(1.5) # Pausa para ver el carrito
    
    # Checkout
    print("Iniciando proceso de pago...")
    boton_checkout = wait.until(EC.element_to_be_clickable((By.ID, "checkout")))
    boton_checkout.click()
    time.sleep(1)
    
    print("Completando datos de envío...")
    driver.find_element(By.ID, "first-name").send_keys("Karen")
    time.sleep(0.5) # Escribe y frena medio segundo
    driver.find_element(By.ID, "last-name").send_keys("Del Pino")
    time.sleep(0.5)
    driver.find_element(By.ID, "postal-code").send_keys("5507")
    time.sleep(1) # Espera un segundo con los datos completos
    
    # --- CAPTURA DE PANTALLA ---
    print("Tomando foto de los datos...")
    driver.save_screenshot("captura_datos.png")
    # ---------------------------

    driver.find_element(By.ID, "continue").click()
    time.sleep(1.5) # Pausa para ver el resumen del pedido
    
    print("Confirmando compra...")
    driver.find_element(By.ID, "finish").click()
    
    mensaje_exito = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))).text
    
    print("-" * 30)
    print(f"RESULTADO CAPTURADO: '{mensaje_exito}'")
    print("-" * 30)
    print("Generando y descargando el PDF del pedido...")
    
    # Buscamos cualquier elemento en la página que contenga el texto "Generate PDF"
    boton_pdf = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Generate PDF')]")))
    boton_pdf.click()

    # Pausa de 5 segundos para dar tiempo a que el navegador genere y descargue el archivo
    time.sleep(5)
    print("¡Descarga de PDF solicitada!")
    
    time.sleep(3) # Pausa final antes de cerrar

finally:
    print("Cerrando navegador.")
    driver.quit()