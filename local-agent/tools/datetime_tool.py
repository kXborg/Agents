from datetime import datetime

schema = {
    "name": "get_datetime",
    "description": "Returns current date and time",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
    }
}

def get_datetime():
    now = datetime.now().isoformat(timespec="seconds")

    return {
        "current_datetime": now
    }

TOOL = {
    "schema": schema,
    "function": get_datetime
}