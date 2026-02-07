import time
import subprocess
import pyautogui

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def activate_chrome():
    subprocess.run(["osascript", "-e", 'tell application "Google Chrome" to activate'])


def get_screen_click_point(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(0.2)

    data = driver.execute_script(
        """
        const el = arguments[0];
        const r = el.getBoundingClientRect();
        return {
          left: r.left,
          top: r.top,
          width: r.width,
          height: r.height,
          screenX: window.screenX,
          screenY: window.screenY,
          outerH: window.outerHeight,
          innerH: window.innerHeight,
          cssScreenW: window.screen.width
        };
        """,
        element,
    )

    chrome_top = data["outerH"] - data["innerH"]

    x_css = data["screenX"] + data["left"] + (data["width"] / 2)
    y_css = data["screenY"] + chrome_top + data["top"] + (data["height"] / 2)

    screen_w_py = pyautogui.size().width
    scale = screen_w_py / data["cssScreenW"]

    x = x_css * scale
    y = y_css * scale
    return x, y


def move_mouse_and_click(driver, element, duration=0.8):
    activate_chrome()
    time.sleep(0.2)

    x, y = get_screen_click_point(driver, element)

    pyautogui.moveTo(x, y, duration=duration)
    time.sleep(0.05)
    pyautogui.click()


def wait_for(driver, by, selector, timeout=20):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, selector)))


def wait_clickable(driver, by, selector, timeout=20):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, selector)))


driver = webdriver.Chrome()
driver.get("https://www.magazineluiza.com.br/")
driver.maximize_window()

wait = WebDriverWait(driver, 20)





# 1) Campo de busca
search_input = wait_clickable(driver, By.ID, "header-search-input", timeout=20)
move_mouse_and_click(driver, search_input, duration=0.7)
search_input.send_keys("iPhone")

# 2) Sugestões
suggestions = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid='suggestion-input-item']"))
)

# 3) Terceiro item
third_item = suggestions[2]
move_mouse_and_click(driver, third_item, duration=0.9)

# 4) Aguarda estabilizar após navegar/atualizar
wait_for(driver, By.ID, "header-search-input", timeout=20)

# 5) Informática
informatic_button = wait_clickable(
    driver,
    By.XPATH,
    "//button[@data-testid='header-link-item' and contains(., 'Informática')]",
    timeout=25,
)
move_mouse_and_click(driver, informatic_button, duration=0.9)

# 6) Notebooks
notebooks_link = wait_clickable(
    driver,
    By.XPATH,
    "//a[@data-testid='dropdown-list-item' and contains(@href, '/notebook/') and contains(., 'Notebooks')]",
    timeout=25,
)
move_mouse_and_click(driver, notebooks_link, duration=0.9)

time.sleep(10)
driver.quit()