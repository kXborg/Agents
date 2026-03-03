import pyautogui
import time
time.sleep(5)
greet_text = "Hello! How is it going?" 
pyautogui.typewrite(greet_text, interval=0.05)
pyautogui.press("enter")
