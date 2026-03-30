import pyautogui
import time
import torch
from PIL import ImageGrab
from transformers import AutoModelForCausalLM, AutoTokenizer

# Setup fail-safes
pyautogui.PAUSE = 2.5
pyautogui.FAILSAFE = True


def load_model(model_name):
    moondream = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, dtype=torch.bfloat16, device_map={"": "cuda"})
    moondream.compile()

    return moondream


def grab_click(query, model):
    # Capture current screen
    screenshot = ImageGrab.grab()  # PIL image
    height = screenshot.height
    width = screenshot.width
    screenshot.save("screen.png")

    # Ask Moondream to locate WhatsApp icon
    response = model.point(screenshot, query)

    print("Model response:", response)

    coords = None
    try:
        point1 = response["points"][0]
        abs_x = int(point1['x'] * width)
        abs_y = int(point1['y'] * height)
        coords = [abs_x, abs_y]
    except Exception:
        print("Could not parse response. Got:", response)

    # Use PyAutoGUI to click
    if coords:
        print(f"Clicking at {coords}")
        pyautogui.moveTo(coords[0], coords[1], duration=0.5)
        pyautogui.click()
    else:
        print("No valid coordinates, skipping click.")

    time.sleep(2)


def main():
    model = load_model("moondream/moondream3-preview")

    grab_click("WhatsApp Icon", model)
    grab_click("Sovit DeepVidya", model)

    screenshot = ImageGrab.grab()

    capt = model.query(screenshot, "What do you think about Sovit's profile pic?")
    ans = capt["answer"]
    print(ans)

    greet_text = "Hi this is my first attempt on Agents!"

    pyautogui.typewrite(greet_text, interval=0.05)
    pyautogui.press("enter")

    pyautogui.typewrite(ans, interval=0.05)
    pyautogui.press("enter")


if __name__ == '__main__':
    main()
