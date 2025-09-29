import io
import re
import time
import json
import torch
import pyautogui
from actions import *
from google import genai
from PIL import Image, ImageGrab
from collections import defaultdict
from transformers import AutoModelForCausalLM, AutoTokenizer


# Setup fail-safes
pyautogui.PAUSE = 2.5
pyautogui.FAILSAFE = True

# Store outputs from actions
action_outputs = defaultdict(dict)


# Placeholder: Gemini 2.5 Flash
def read_text_from_image_gemini(client, query):
    screen_capture = ImageGrab.grab() 
    # Convert to bytes
    img_bytes_io = io.BytesIO()
    screen_capture.save(img_bytes_io, format="PNG") 
    img_bytes = img_bytes_io.getvalue()

    # Send request
    print('Calling Gemini 2.5 Flash ..')
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            {
                "role": "user",
                "parts": [
                    {"text": query},
                    {"inline_data": {"mime_type": "image/png", "data": img_bytes}},
                ],
            }
        ],
    )

    return response.text


def get_action_plan(client, prompt):
    system_prompt = f"""
    You are a gui-native agent planner. Convert the user's instruction into a JSON action plan.
    Use only the following action schema: 
      - read_text_from_image_gemini(client, query) 
      - locate_object_moondream(target_obj, model)
      - click(x=None, y=None, button="left")
      - double_click(x=None, y=None)
      - right_click(x=None, y=None)
      - move_mouse(x, y, duration=0.2)
      - press_key(key)
      - hotkey(*keys)
      - type_text(text)
      - clear_field()
      - launch_app(path)
      - sleep(seconds=None)

    Pre-defined paths (args) for launch_app action:
      - "whatsapp" → will resolve to whatsapp://
      - "chrome"   → C:/Program Files/Google/Chrome/Application/chrome.exe
      - "edge"     → C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe
      - "sublime"  → C:/Program Files/Sublime Text/sublime_text.exe
      - "slack"    → C:/Users/<YourUser>/AppData/Local/slack/slack.exe
      - "telegram" → C:/Users/<YourUser>/AppData/Roaming/Telegram Desktop/Telegram.exe
      - "vscode"   → C:/Users/<YourUser>/AppData/Local/Programs/Microsoft VS Code/Code.exe


    Apps other than predefined paths are to be searched onscreen or searched from start menu. Understanding image is for Gemini and locating objects P(x,y) is for Moondream.
    Sleep time is in seconds. Always start by capturing screen, analysing what's on it, then move on to the next actions. Screen capture for image processing functions are inbuilt using PIL.
    For whatsApp or Google Chrome, once the app is open, you can start typing name directly. It will type in the search bar. No need to locate the search bar. 
    But make sure to locate Name(with round profile pic on left) before sending message. Add 2s delay after opening the application.

    Each action must be a JSON object with keys:
      - "action": action name
      - "args": dictionary of arguments for that action
    
    Only output JSON array of actions. Do not include explanations or extra text.
    
    Instruction:
    {prompt}
    """
    print('Generating Action Plan. Please wait ...')

    # Call Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[{"role": "user", "parts": [{"text": system_prompt}]}],
    )
    print('✅ Done.')

    # Access text properly
    try:
        raw_text = response.candidates[0].content.parts[0].text.strip()

        # Remove Markdown fences if present
        raw_text = re.sub(r"^```(?:json)?|```$", "", raw_text, flags=re.MULTILINE).strip()

        # Now directly parse JSON
        action_plan = json.loads(raw_text)

        # Validate schema
        for i, step in enumerate(action_plan):
            if "action" not in step or "args" not in step:
                print(f"⚠️ Step {i} missing required keys:", step)

        return action_plan

    except Exception as e:
        print("❌ Error generating action plan:", e)
        print("Response text:", raw_text[:500])  # preview first 500 chars
        return []



def substitute_vars(arg_value):
    """
    Replace placeholders like {{var_name}} or {{var_name.key}} with actual values from action_outputs.
    Works recursively for lists and dicts.
    """
    if isinstance(arg_value, str):
        matches = re.findall(r"{{(.*?)}}", arg_value)
        for m in matches:
            parts = m.split(".")
            var_name = parts[0]
            key = parts[1] if len(parts) > 1 else None
            value = action_outputs.get(var_name, {})
            if key:
                value = value.get(key, "")
            arg_value = arg_value.replace(f"{{{{{m}}}}}", str(value))
        return arg_value
    elif isinstance(arg_value, list):
        return [substitute_vars(v) for v in arg_value]
    elif isinstance(arg_value, dict):
        return {k: substitute_vars(v) for k, v in arg_value.items()}
    else:
        return arg_value



def execute_actions(action_plan):
    """
    Execute a list of actions (from get_action_plan).
    """
    for step in action_plan:
        action_name = step.get("action")
        args = step.get("args", {})
        output_var = step.get("output")  # Optional output variable

        # Substitute variables in args
        args = {k: substitute_vars(v) for k, v in args.items()}

        try:
            result = None

            if action_name == "click_target":
                target = args["target"]
                coords = locate_object_moondream(target_obj, moondream)
                if coords:
                    click(coords["x"], coords["y"])
                    result = coords
                else:
                    print(f"❌ Could not locate {target}")

            elif action_name == "read_text_from_image_gemini":
                query = args.get("prompt", "")
                result_text = read_text_from_image_gemini(client, query)
                result = {"text": result_text}

            elif action_name == "locate_object_moondream":
                desc = args["target_obj"]
                coords = locate_object_moondream(desc, moondream)
                result = coords if coords else {}

            elif action_name == "launch_app":
                app_path = args.get("path")
                launch_app(app_path)
                result = {"status": "launched"}

            else:
                # Map to local functions if available
                func = globals().get(action_name)
                if func:
                    result = func(**args) if args else func()
                else:
                    print(f"⚠️ Unknown action: {action_name}")

            # Store result in outputs if specified
            if output_var:
                action_outputs[output_var] = result

            print(f"✅ Executed {action_name}, output: {result}")

        except Exception as e:
            print(f"❌ Error executing {action_name}: {e}")



# Example Usage
if __name__ == "__main__":
    time.sleep(0.5)
    # Load Gemini Client
    client = genai.Client()

    # Load Moondream 3 preview Model
    model_name = "moondream/moondream3-preview"
    moondream = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, dtype=torch.bfloat16, device_map={"": "cuda"})
    moondream.compile()

    # Task prompt
    task_to_do = "Hi please check in 5s interval if classifier training is complete from the jupyter notebook on screen, if yes text Kukil Kashyap Borgohain on WhatsApp and share training statistics."

    # Get action plan from Gen Model
    action_pln = get_action_plan(client, task_to_do)
    print(action_pln)

    execute_actions(action_pln)