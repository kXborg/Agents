import pyautogui
import time
import torch
from PIL import ImageGrab
from transformers import AutoModelForCausalLM, AutoTokenizer


def load_model(model_name):
    moondream = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, dtype=torch.bfloat16, device_map={"": "cuda"})
    moondream.compile()

    return moondream


def main():
    model = load_model("moondream/moondream3-preview")

    # Capture current screen
    screenshot = ImageGrab.grab()  # PIL image
    screenshot.save("screen.png")

    # Ask Moondream to locate WhatsApp icon
    query = "WhatsApp Icon"
    response = model.point(screenshot, query)

    print("Model response:", response)

    {'points': [{'x': 0.294921875, 'y': 0.9794921875}]}

    

    abs_x = int(point['x'] * width)
    abs_y = int(point['y'] * height)

    coords = None
    try:
        coords = (int(response["x"]), int(response["y"]))
    except Exception:
        print("Could not parse response. Got:", response)

    # # --- 4. Use PyAutoGUI to click ---
    # if coords:
    #     print(f"Clicking at {coords}")
    #     pyautogui.moveTo(coords[0], coords[1], duration=0.5)
    #     pyautogui.click()
    # else:
    #     print("No valid coordinates, skipping click.")

    # # --- 5. (Optional) Type message ---
    # time.sleep(2)  # wait for chat to open
    # pyautogui.typewrite("Happy Birthday!", interval=0.05)
    # pyautogui.press("enter")

if __name__ == '__main__':
    main()
