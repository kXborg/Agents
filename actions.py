import pyautogui
import pyperclip
import pygetwindow as gw
import pytesseract
import psutil
import os
import time
from PIL import Image, ImageGrab

predefined_paths = {
    "whatsapp": "whatsapp://",
    "chrome": "C:/Program Files/Google/Chrome/Application/chrome.exe",
    "edge": "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
    "sublime text": "C:/Program Files/Sublime Text 3/sublime_text.exe"
}


def scroll(amount):
    """Scroll vertically (positive=up, negative=down)."""
    pyautogui.scroll(amount)


def move_mouse(x, y, duration=0.2):
    pyautogui.moveTo(x, y, duration=duration)


def click(x=None, y=None, button="left"):
    pyautogui.click(x, y, button=button)


def double_click(x=None, y=None):
    pyautogui.doubleClick(x, y)


def right_click(x=None, y=None):
    pyautogui.rightClick(x, y)


def drag_and_drop(x1, y1, x2, y2, duration=0.5):
    pyautogui.moveTo(x1, y1)
    pyautogui.dragTo(x2, y2, duration=duration)


def press_key(key):
    pyautogui.press(key)


def hotkey(*keys):
    pyautogui.hotkey(*keys)


def type_text(text):
    pyautogui.typewrite(text, interval=0.05)


def clear_field():
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")


# def launch_app(path):
#     try:
#         # Resolve path if it's a predefined app
#         resolved_path = predefined_paths.get(path.lower(), path)
#         os.startfile(resolved_path)
#         print(f"✅ Launched {path}")
#     except Exception as e:
#         print(f"❌ Could not launch {path}: {e}")


def launch_app(path):
    """
    Launch an application with a contingency:
    1. Try predefined path / os.startfile
    2. If fails, open Start menu, type app name, press Enter
    3. Verify app launch using Moondream
    """
    resolved_path = predefined_paths.get(path.lower(), path)
    try:
        os.startfile(resolved_path)
        print(f"✅ Launched {path} via predefined path")
        time.sleep(2)
        return True
    except Exception as e:
        print(f"❌ Could not launch {path} via predefined path: {e}")
        print(f"⚡ Attempting Start Menu fallback...")

        try:
            # Open Start menu (Windows key)
            pyautogui.press("win")
            time.sleep(1)

            # Type the app name
            pyautogui.typewrite(path, interval=0.05)
            time.sleep(0.5)

            # Press Enter
            pyautogui.press("enter")
            time.sleep(3)  # give it some time to launch

        except Exception as ex:
            print(f"❌ Start menu fallback failed for {path}: {ex}")
            return False


def is_process_running(name):
    """Check if process is running by name."""
    return any(name.lower() in p.name().lower() for p in psutil.process_iter())

def kill_process(name):
    for p in psutil.process_iter():
        if name.lower() in p.name().lower():
            p.terminate()
            return True
    return False

def sleep(seconds=None):
    """Pause execution for N seconds"""
    if seconds is not None:
        time.sleep(seconds)

