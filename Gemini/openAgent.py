from actions import *
from tqdm import tqdm
from google import genai
import pyautogui, threading
from PIL import Image, ImageGrab
from collections import defaultdict
import io, os, re, time, json, torch, argparse
from transformers import AutoModelForCausalLM, AutoTokenizer


# Setup fail-safes
pyautogui.PAUSE = 2.5
pyautogui.FAILSAFE = True

# Store outputs from actions
action_outputs = defaultdict(dict)

predefined_paths = {
    "whatsapp": "whatsapp://",
    "chrome": "C:/Program Files/Google/Chrome/Application/chrome.exe",
    "edge": "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
    "sublime text": "C:/Program Files/Sublime Text 3/sublime_text.exe"
}


def read_text_from_image_gemini(client, query):
    # Capture screen
    screen_capture = ImageGrab.grab() 

    # Convert to bytes
    img_bytes_io = io.BytesIO()
    screen_capture.save(img_bytes_io, format="PNG") 
    img_bytes = img_bytes_io.getvalue()

    # Event to stop the progress bar
    stop_event = threading.Event()

    # Progress bar function
    def progress_task(stop_event):
        with tqdm(total=100, bar_format="⏳ Waiting for Gemini 2.5 Flash... {bar} {elapsed}") as pbar:
            while not stop_event.is_set():
                time.sleep(0.1)  # simulate waiting
                pbar.update(1)
                if pbar.n >= pbar.total:  # loop the bar
                    pbar.n = 0
                    pbar.last_print_n = 0
            pbar.close()

    # Start progress bar in a daemon thread
    thread = threading.Thread(target=progress_task, args=(stop_event,), daemon=True)
    thread.start()

    # Send request to Gemini
    try:
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
            config=genai.types.GenerateContentConfig(thinking_config=genai.types.ThinkingConfig(thinking_budget=0))
        )
    finally:
        # Stop progress bar
        stop_event.set()
        thread.join()

    return response.text


def get_action_plan(client, prompt):
    system_prompt = f"""
    You are a gui-native agent planner. Convert the user's instruction into a JSON action plan.
    Use only the following action schema: 
      - read_text_from_image_gemini(client, query) 
      - locate_object(target_obj, client)
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
      - scroll(amount)

    Pre-defined paths (args) for launch_app action, windows specific:
      - "whatsapp" → will resolve to whatsapp://
      - "chrome"   → C:/Program Files/Google/Chrome/Application/chrome.exe
      - "edge"     → C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe
      - "sublime text" → "C:/Program Files/Sublime Text 3/sublime_text.exe"

    Apps other than predefined paths are to be searched onscreen or searched from start menu.
    Sleep time is in seconds. Always start by capturing screen, analysing what's on it, then move on to the next actions. 
    Add 2s delay after opening the application. For WhatsApp or Telegram or other chat apps, once the app is open, start typing the user name directly. Press down arrow, enter, then type message, finally hit enter to send.close the app using Alt + F4 hotkey.
    For Chrome or other browser like application, type URL after opening the app directly. No need to find searchbar and click to type.

    Sublime scheme:
      - Once editing is done, save using hotkey Ctrl + S, type in file name, hit enter
      - close the app using Alt + F4 hotkey

    Page reading scheme:
      - If it is about reading page on chrome, move_mouse to center of chrome window (use locate_object() function to get that point), Capture first screen and read. > store summary
      - Scrolldown the page by -900 units.
      - Capture screen and read using read_text_from_image_gemini. > store summary
      - Repeat scroll > Capture > read page untill end of page is reached. 
      - End of the page can be seen when scroll bar on right has reached bottom of the window.
      - Finally create a single summary out of all images read so far.

    The function locate_object(target_obj, client) is using Gemini client to locate objects on screen. 
    
    IMPORTANT: 
      - Any information retrieved from 'read_text_from_image_gemini' should be referenced in subsequent actions using the placeholder <OUTPUT_FROM_read_text_from_image_gemini>. Do NOT write fixed summaries. 
      - Any information retrieved from 'locate_object' should be referenced in subsequent actions using the placeholder <OUTPUT_FROM_locate_object>.
      - The placeholders will be replaced at runtime with the actual output. 
      - Do NOT attempt to reference x/y coordinates from text output.
      - Do no summarise the powershell window or terminal window open on the right side of the screen.
    
    Each action must be a JSON object with keys:
      - "action": action name
      - "args": dictionary of arguments for that action
    
    Only output JSON array of actions. Do not include explanations or extra text.
    
    Instruction:
    {prompt}
    """
    # print('Generating Action Plan. Please wait ...')

    # Event to stop progress bar
    stop_event = threading.Event()

    # Progress bar function
    def progress_task(stop_event):
        with tqdm(total=100, bar_format="\033[92m⏳ Generating Action Plan... {bar} {percentage:3.0f}% | {elapsed}\033[0m") as pbar:
            while not stop_event.is_set():
                time.sleep(0.4)
                pbar.update(1)
                if pbar.n >= pbar.total:  # loop the bar
                    pbar.n = 0
                    pbar.last_print_n = 0
            pbar.close()

    # Start progress bar in a separate daemon thread
    thread = threading.Thread(target=progress_task, args=(stop_event,), daemon=True)
    thread.start()

    try:
        # Call Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[{"role": "user", "parts": [{"text": system_prompt}]}],
        )
    finally:
        # Stop progress bar
        stop_event.set()
        thread.join()

    print('✅ Done.')

    # Access text properly
    try:
        raw_text = response.candidates[0].content.parts[0].text.strip()
        raw_text = re.sub(r"^```(?:json)?|```$", "", raw_text, flags=re.MULTILINE).strip()
        action_plan = json.loads(raw_text)

        # Validate schema
        for i, step in enumerate(action_plan):
            if "action" not in step or "args" not in step:
                print(f"⚠️ Step {i} missing required keys:", step)

        return action_plan

    except Exception as e:
        print("❌ Error generating action plan:", e)
        print("Response text:", raw_text[:500])
        return []


def substitute_vars(arg_value):
    if isinstance(arg_value, str):
        # Existing {{var.key}} replacement
        matches = re.findall(r"{{(.*?)}}", arg_value)
        for m in matches:
            parts = m.split(".")
            var_name = parts[0]
            key = parts[1] if len(parts) > 1 else None
            value = action_outputs.get(var_name, {})
            if key:
                value = value.get(key, "")
            arg_value = arg_value.replace(f"{{{{{m}}}}}", str(value))

        # Replace Gemini read placeholder
        if "<OUTPUT_FROM_read_text_from_image_gemini>" in arg_value:
            gemini_output = action_outputs.get("read_text_from_image_gemini", {}).get("text", "")
            arg_value = arg_value.replace("<OUTPUT_FROM_read_text_from_image_gemini>", gemini_output)

        # ✅ Replace locate_object placeholders
        loc_matches = re.findall(r"<OUTPUT_FROM_locate_object\.(.*?)>", arg_value)
        for key in loc_matches:
            loc_output = action_outputs.get("locate_object", {})
            value = loc_output.get(key, "")
            arg_value = arg_value.replace(f"<OUTPUT_FROM_locate_object.{key}>", str(value))

        return arg_value

    elif isinstance(arg_value, list):
        return [substitute_vars(v) for v in arg_value]
    elif isinstance(arg_value, dict):
        return {k: substitute_vars(v) for k, v in arg_value.items()}
    else:
        return arg_value


def execute_actions(action_plan, client):
    """
    Execute a list of actions (from get_action_plan) safely.
    Handles dynamic placeholders and stores outputs for later substitution.
    """
    for step in action_plan:
        action_name = step.get("action")
        args = step.get("args", {})
        output_var = step.get("output")  # Optional output variable

        # Substitute placeholders dynamically
        args = {k: substitute_vars(v) for k, v in args.items()}

        try:
            result = None

            if action_name in ["click", "double_click", "right_click", "move_mouse"]:
                # Ensure numeric coordinates
                x = int(args.get("x", 0)) if args.get("x") is not None else None
                y = int(args.get("y", 0)) if args.get("y") is not None else None

                if action_name == "click":
                    pyautogui.click(x=x, y=y, button=args.get("button", "left"))
                elif action_name == "double_click":
                    pyautogui.doubleClick(x=x, y=y)
                elif action_name == "right_click":
                    pyautogui.rightClick(x=x, y=y)
                elif action_name == "move_mouse":
                    duration = float(args.get("duration", 0.2))
                    pyautogui.moveTo(x, y, duration=duration)

                result = {"x": x, "y": y}

            elif action_name == "click_target":
                target = args["target"]
                coords = locate_object(target, client)
                if coords:
                    first_point = coords[0]
                    pyautogui.click(first_point["x"], first_point["y"])
                    result = first_point
                    # Store for placeholder substitution
                    action_outputs["locate_object"] = first_point
                else:
                    print(f"❌ Could not locate target: {target}")

            elif action_name == "locate_object":
                target = args["target_obj"]
                coords = locate_object(target, client)
                result = coords[0] if coords else {}
                # Store first point for placeholders
                action_outputs["locate_object"] = result

            elif action_name == "read_text_from_image_gemini":
                query = args.get("query", "")
                result_text = read_text_from_image_gemini(client, query)
                result = {"text": result_text}
                # Store output for placeholder substitution
                action_outputs["read_text_from_image_gemini"] = result

            elif action_name == "launch_app":
                app_path = args.get("path")
                launch_app(app_path)
                time.sleep(2)
                result = {"status": "launched"}

            elif action_name == "hotkey":
                keys = args.get("keys", [])
                if isinstance(keys, list):
                    pyautogui.hotkey(*keys)
                    result = {"pressed": keys}
                else:
                    print(f"❌ Invalid keys argument for hotkey: {keys}")

            elif action_name == "type_text":
                text = args.get("text", "")
                type_text(text)
                result = {"typed": text}

            elif action_name == "press_key":
                key = args.get("key")
                press_key(key)
                result = {"pressed": key}

            elif action_name == "clear_field":
                clear_field()
                result = {"status": "cleared"}

            elif action_name == "sleep":
                seconds = float(args.get("seconds", 1))
                time.sleep(seconds)
                result = {"slept": seconds}

            elif action_name == "scroll":
                amount = int(args.get("amount", 0))
                pyautogui.scroll(amount)
                result = {"scrolled": amount}

            else:
                # Map to any other local function if available
                func = globals().get(action_name)
                if func:
                    result = func(**args) if args else func()
                else:
                    print(f"⚠️ Unknown action: {action_name}")

            # Store output in outputs dict
            if output_var:
                action_outputs[output_var] = result

            print(f"✅ Executed {action_name}, output: {result}")
            # print(f"✅ Executed {action_name}")

        except Exception as e:
            print(f"❌ Error executing {action_name}: {e}")



def locate_object(target_obj, client):
    screen_capture = ImageGrab.grab()
    width, height = screen_capture.size

    # Convert image to bytes
    img_bytes_io = io.BytesIO()
    screen_capture.save(img_bytes_io, format="PNG")
    img_bytes = img_bytes_io.getvalue()

    prompt = (
        f"You are given a screenshot. Find all instances of '{target_obj}' on the image. "
        "Return a JSON array of objects with 'x', 'y', and optional 'confidence' fields, "
        "where x and y are normalized coordinates (0 to 1, top-left origin). "
        "Do NOT return any text outside the JSON."
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[{
            "role": "user",
            "parts": [
                {"text": prompt},
                {"inline_data": {"mime_type": "image/png", "data": img_bytes}},
            ],
        }]
    )

    points_list = []
    try:
        response_text = response.text if hasattr(response, "text") else str(response)

        # Strip Markdown code fences
        cleaned_text = re.sub(r"^```json\s*|```$", "", response_text.strip(), flags=re.MULTILINE)

        points = json.loads(cleaned_text)
        for point in points:
            x = int(point["x"] * width)
            y = int(point["y"] * height)
            confidence = point.get("confidence", 1.0)
            points_list.append({"x": x, "y": y, "confidence": confidence})

        return points_list

    except Exception as e:
        print("Failed to parse points from Gemini response:", e)
        print("Raw response:", response_text)
        return []


if __name__ == "__main__":
    time.sleep(0.5)

    parser = argparse.ArgumentParser(description="Agentic Action Plan Executor")
    parser.add_argument(
        "--task",
        type=str,
        required=True,
        help="Task prompt in natural language, e.g., 'Summarize screen content and send report via WhatsApp'"
    )
    args = parser.parse_args()
    task_to_do = args.task

    client = genai.Client()

    # Get action plan from Gemini
    # print("📝 Generating action plan ...")
    action_pln = get_action_plan(client, task_to_do)
    print("📋 Action plan:", action_pln)

    # 5. Execute actions
    execute_actions(action_pln, client)