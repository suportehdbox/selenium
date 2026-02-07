import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://www.magazineluiza.com.br/")
driver.maximize_window()

wait = WebDriverWait(driver, 15)
actions = ActionChains(driver)

# Campo de busca
search_input = wait.until(
    EC.element_to_be_clickable((By.ID, "header-search-input"))
)
search_input.click()
search_input.send_keys("iPhone")

# Lista de sugestões
suggestions = wait.until(
    EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "[data-testid='suggestion-input-item']")
    )
)

# Terceiro item
third_item = suggestions[2]
actions.move_to_element(third_item).pause(0.6).click(third_item).perform()

time.sleep(10)

# Clica em "Informática"
informatic_button = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//button[@data-testid='header-link-item' and contains(., 'Informática')]")
    )
)
actions.move_to_element(informatic_button).pause(0.4).click(informatic_button).perform()

# Clica no item do dropdown "Notebooks"
notebooks_link = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//a[@data-testid='dropdown-list-item' and contains(@href, '/notebook/') and contains(., 'Notebooks')]")
    )
)
actions.move_to_element(notebooks_link).pause(0.3).click(notebooks_link).perform()

time.sleep(10)
driver.quit()