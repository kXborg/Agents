from langchain_core.messages import SystemMessage
from scripts.repo_parser.tools.parse_python import parse_python
from scripts.repo_parser.tools.parse_markdown import parse_markdown
from scripts.repo_parser.tools.parse_notebook import parse_notebook
from scripts.repo_parser.tools.parse_json_yaml import parse_json_yaml
from scripts.repo_parser.utils.fetch_blob import fetch_blob_content

# Tool registry
PARSERS = {
    ".py": parse_python,
    ".md": parse_markdown,
    ".txt": parse_markdown,
    ".json": parse_json_yaml,
    ".yaml": parse_json_yaml,
    ".yml": parse_json_yaml,
    ".ipynb": parse_notebook,
}

async def fetch_and_parse_node(state: dict) -> dict:
    """
    Fetches file content for 'selected_files' and parses each file using
    the appropriate tool for its extension.

    Output stored in:
      state["parsed_files"] = [{"path": ..., "parsed": ...}, ...]
    """

    print("Initializing Fetch & Parse Node...")

    selected_files = state.get("selected_files", [])
    if not selected_files:
        return {
            **state,
            "parsed_files": [],
            "messages": state.get("messages", []) + [
                SystemMessage(content="No files selected for parsing.")
            ]
        }

    parsed_results = []

    for file_meta in selected_files:
        path = file_meta["path"]
        ext = file_meta["ext"].lower()
        url = file_meta["url"]

        print(f"Fetching file: {path}")

        # Fetch file content from GitHub
        raw_content = fetch_blob_content(url)
        if not raw_content:
            parsed_results.append({
                "path": path,
                "parsed": f"<Failed to fetch content for {path}>"
            })
            continue

        # Select parser based on extension
        parser_fn = PARSERS.get(ext, None)

        if parser_fn:
            try:
                print("Checking Execution of parser tools")
                parsed = parser_fn(raw_content)
            except Exception as e:
                parsed = f"<Error parsing file {path}: {e}>"
        else:
            parsed = raw_content[:5000]  # token-safe limit

        parsed_results.append({
            "path": path,
            "ext": ext,
            "parsed": parsed
        })
    print(f"Parsed {len(parsed_results)} files.")

    return {
        **state,
        "parsed_files": parsed_results,
        "messages": state.get("messages", []) + [
            SystemMessage(content=f"Fetched & parsed {len(parsed_results)} files.")
        ]
    }
