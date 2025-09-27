import io
import pyautogui
from google import genai

client = genai.Client(api_key="AIzaSyB6caWuNx4uYKrNXQWVgXzJOcGxIJdJYSs")

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
                {"text": "is the model training complete in the jupyter notebook? Answer in Yes or No."},
                {"inline_data": {"mime_type": "image/png", "data": img_bytes}},
            ],
        }
    ],
)

print(response.text)
