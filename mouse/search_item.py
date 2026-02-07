import pyautogui
import time

time.sleep(3)  # tempo pra você focar a janela do Chrome
pyautogui.moveTo(600, 220, duration=1)  # coordenadas na tela
pyautogui.click()