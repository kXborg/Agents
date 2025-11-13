# nodes/fetch_repo_metadata_node.py

from langchain_core.messages import SystemMessage
from scripts.repo_parser.github_repo_parser import GitRepoParser

async def fetch_repo_metadata_node(state: dict) -> dict:
    """
    First node of the workflow:
    - Reads repository URL from state['url']
    - Calls GitRepoParser to get metadata tree
    - Updates state with repo_tree
    """

    print("Initializing Fetch Repo Metadata Node...")

    repo_url = state.get("url", None)
    if not repo_url:
        return {
            **state,
            "messages": state.get("messages", []) + [
                SystemMessage(content="No repository URL provided.")
            ]
        }

    try:
        parser = GitRepoParser()
        repo_tree = parser.get_dir_tree(repo_url)

        print("Repo metadata tree fetched successfully!")

        return {
            **state,
            "repo_tree": repo_tree,
            "messages": state.get("messages", []) + [
                SystemMessage(content=f"Fetched metadata tree for: {repo_url}")
            ]
        }

    except Exception as e:
        err = f"Error fetching repository metadata: {e}"
        print(err)
        return {
            **state,
            "repo_tree": {},
            "messages": state.get("messages", []) + [
                SystemMessage(content=err)
            ]
        }
