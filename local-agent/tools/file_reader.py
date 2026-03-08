import os

# Project root = two levels up from this file (tools/file_reader.py -> project root)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

schema = {
    "name": "read_file",
    "description": "Reads the content of a text file given its file path within the project directory.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the file to read (relative to project root)"
            }
        },
        "required": ["file_path"]
    }
}

def read_file(file_path):
    # Resolve to absolute path (handles both relative and absolute inputs)
    abs_path = os.path.abspath(os.path.join(PROJECT_ROOT, file_path))

    # Security check: must be within project root
    if not abs_path.startswith(PROJECT_ROOT):
        return {"error": "Access denied. Can only read files within the project directory."}

    if not os.path.exists(abs_path):
        return {"error": f"File not found: {file_path}"}

    try:
        with open(abs_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"content": content}
    except Exception as e:
        return {"error": str(e)}

TOOL = {
    "schema": schema,
    "function": read_file
}
