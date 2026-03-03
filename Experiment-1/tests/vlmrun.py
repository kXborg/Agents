import io
import time
import torch
import pyautogui
from PIL import ImageGrab
from google import genai 
from transformers import AutoModelForCausalLM, AutoTokenizer

# Setup fail-safes
pyautogui.PAUSE = 2.5
pyautogui.FAILSAFE = True

client = genai.Client()


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
        pyautogui.moveTo(coords[0], coords[1], duration=0.2)
        pyautogui.click()
    else:
        print("No valid coordinates, skipping click.")

    time.sleep(2)


def gemini_call(img):
    # Convert to bytes
    img_bytes_io = io.BytesIO()
    img.save(img_bytes_io, format="PNG") 
    img_bytes = img_bytes_io.getvalue()

    # Send request
    print('Calling Gemini 2.5 Flash ..')
    short_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            {
                "role": "user",
                "parts": [
                    {"text": "Is the model training complete in the jupyter notebook? Answer in Yes or No."},
                    {"inline_data": {"mime_type": "image/png", "data": img_bytes}},
                ],
            }
        ],
    )

    # Send request
    print('Calling Gemini 2.5 Flash ..')
    long_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            {
                "role": "user",
                "parts": [
                    {"text": "Is the model training complete? If yes generate a report of final accuracies within 100 words."},
                    {"inline_data": {"mime_type": "image/png", "data": img_bytes}},
                ],
            }
        ],
    )

    s_ans = short_response.text
    l_ans = long_response.text

    return s_ans, l_ans



def main():
    model = load_model("moondream/moondream3-preview")

    screenshot = ImageGrab.grab()

    short_ans, long_ans = gemini_call(screenshot)
    print(short_ans)
    print(type(short_ans))

    if 'yes' in short_ans.lower(): 
        grab_click("WhatsApp Icon", model)
        grab_click("Kukil Kashyap Borgohain", model)

        pyautogui.typewrite(long_ans, interval=0.05)
        pyautogui.press("enter")


if __name__ == '__main__':
    main()
