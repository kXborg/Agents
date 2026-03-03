import io
import pyautogui
from google import genai

client = genai.Client(api_key="AIzaSyBBSLU77PES2mVDy049pvwppKe-HVFJrzo")

# Capture screenshot
screenshot = pyautogui.screenshot()

# Convert to bytes
img_bytes_io = io.BytesIO()
screenshot.save(img_bytes_io, format="PNG")  # could also be "JPEG"
img_bytes = img_bytes_io.getvalue()

# Send request with text + screenshot
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        {
            "role": "user",
            "parts": [
                {"text": "Describe the image in 100 words"},
                {"inline_data": {"mime_type": "image/png", "data": img_bytes}},
            ],
        }
    ],
)

print(response.text)


# from google.api_core.client_options import ClientOptions
# from google.generativeai import Client as GAClient

# api_key = "AIzaSyBBSLU77PES2mVDy049pvwppKe-HVFJrzo"
# client = GAClient(api_key=api_key)

# # Test a simple request
# response = client.generate_text(prompt="Hello world", max_output_tokens=10)
# print(response.text)
