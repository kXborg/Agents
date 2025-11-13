import re
from langchain_core.messages import SystemMessage, HumanMessage

from scripts.repo_parser.utils.flatten_tree import flatten_tree
from scripts.repo_parser.config.settings import MAX_SIZE_KB, IMPORTANT_EXT, IMPORTANT_NAMES

async def analyze_tree_node(state: dict) -> dict:
    """
    Query-aware Analyze Node.
    Decides which files to parse deeply based on:
      - repo metadata
      - user query (latest HumanMessage)
      - file importance (README, setup, main, config, etc.)
      - file sizes and extensions
    """

    print("Initializing Analyze Tree Node...")

    repo_tree = state.get("repo_tree", None)
    if not repo_tree:
        return {**state,
                "selected_files": [],
                "messages": state.get("messages", []) + [
                    SystemMessage(content="No repository tree available.")
                ]}

    flattened = flatten_tree(repo_tree)

    user_query = ""
    for msg in reversed(state.get("messages", [])):
        if isinstance(msg, HumanMessage):
            user_query = msg.content.lower()
            break

    print(f"Latest user query: {user_query}")

    # Get words like ["train", "metrics", "dataset", "model"]
    query_keywords = re.findall(r"[a-zA-Z_]+", user_query)
    print(f"Extracted query keywords: {query_keywords}")

    selected, skipped = [], []

    for meta in flattened:
        path = meta["path"].lower()
        size = meta["size_kb"]
        ext  = meta["ext"].lower()

        # Skip too-large files
        if size > MAX_SIZE_KB:
            skipped.append(path)
            continue

        # Always include important names
        if any(key in path for key in IMPORTANT_NAMES):
            selected.append(meta)
            continue

        # Include files matching keywords in user query
        if any(key in path for key in query_keywords):
            selected.append(meta)
            continue

        # Keep primary code/documentation files
        if ext in IMPORTANT_EXT:
            selected.append(meta)
        else:
            skipped.append(path)

    print(f"Selected {len(selected)} files, skipped {len(skipped)}.")

    return {
        **state,
        "selected_files": selected,
        "skipped_files": skipped,
        "messages": state.get("messages", []) + [
            SystemMessage(content=f"Selected {len(selected)} files based on query: '{user_query}'.")
        ]
    }
