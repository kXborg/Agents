import os

# project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

schema = {
    "name": "list_dir",
    "description": "Enlist the files and folders within a directory, given its folder path within the project directory",
    "parameters": {
        "type": "object",
        "properties": {
            "folder_path": {
                "type": "string",
                "description": "The path to the directory in which subfolders and files to be enlisted (relative to project root)"
            }
        },
        "required": ["folder_path"]
    }
}

def list_dir(folder_path):
    # Resolve to absolute path
    abs_path = os.path.abspath(os.path.join(PROJECT_ROOT, folder_path))

    # Security check
    if not abs_path.startswith(PROJECT_ROOT):
        return {"error": "Access denied. Can only navigate within project root directory"}
    
    if not os.path.exists(abs_path):
        return {"error": f"Directory not found: {abs_path}"}
    
    try:
        contents = os.listdir(abs_path)
        return {"contents": contents}
    
    except Exception as e:
        return {"error ": str(e)}


TOOL = {
    "schema": schema,
    "function": list_dir
}