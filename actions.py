import pyautogui
import pyperclip
import pygetwindow as gw
import pytesseract
import psutil
import os
import time
from PIL import Image, ImageGrab


def locate_object_moondream(target_obj, model, rank=2):
    """
    Locate an object with Moondream.
    By default, returns the 2nd top-left-most point (rank=2).
    You can change `rank` to get the 1st, 3rd, etc.
    """
    # Capture current screen
    screen_capture = ImageGrab.grab()  # PIL image
    height, width = screen_capture.height, screen_capture.width
    screen_capture.save("screen.png")

    # Ask Moondream to locate the target object
    response = model.point(screen_capture, target_obj)
    print("Model response:", response)

    try:
        points = response.get("points", [])
        if not points:
            raise ValueError("No points returned")

        # Sort by top-left priority (min y, then min x)
        sorted_points = sorted(points, key=lambda p: (p['y'], p['x']))

        if len(sorted_points) < rank:
            raise IndexError(f"Less than {rank} points returned")

        # Pick the Nth top-left-most point
        point = sorted_points[rank - 1]

        abs_x = int(point['x'] * width)
        abs_y = int(point['y'] * height)

        return {"x": abs_x, "y": abs_y}

    except Exception as e:
        print("Could not parse response. Got:", response, "Error:", e)
        return None



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

def launch_app(path):
    try:
        if path == "whatsapp":
            os.startfile("whatsapp://")  # this opens WhatsApp if protocol registered
        else:
            os.startfile(path)
        print(f"✅ Launched {path}")
    except Exception as e:
        print(f"❌ Could not launch {path}: {e}")

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

