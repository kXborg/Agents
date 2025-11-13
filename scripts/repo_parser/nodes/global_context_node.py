import base64
import requests
from langchain_core.messages import SystemMessage, HumanMessage
from scripts.repo_parser.utils.flatten_tree import flatten_tree

async def global_context_node(state: dict)->dict: #AgentState)->AgentState
    """
    This node builds a global overview of the repository based 
    on metadata tree fetched from GitRepoParser object. 
    Produces a brief summary of repo structure, key folders and 
    relationships.
    """

    print("-----Initializing Global Context Node-----")
    # print("state variable", state)
    repo_tree = state.get("repo_tree")
    # print(f"repo_tree contains: {repo_tree}")
    if not repo_tree:
        print("No repo tree found in the state")
        return {**state, "global_context": "No repo structure available"}
    
    flattened = flatten_tree(repo_tree)
    # print("flattened tree struture: ", flattened)
    imp_file = [
        f for f in flattened if any(
            kw in f["path"].lower() for kw in [
                "README", "setup", "main", "app", "requirements", "scripts", "configs"
            ]
        )
    ][:5]
    headers = []

    for file_meta in imp_file:
        try:
            file_data = requests.get(file_meta["url"]).json()
            content_b64 = file_data.get("content", "")
            decoded = base64.b64decode(content_b64).decode("utf-8", errors="ignore")
            snippet = "\n".join(decoded.splitlines()[:10])
            headers.append(f"{file_meta['path']}:\n{snippet}\n")
        except Exception as e:
            headers.append(f"{file_meta['path']}: <Error in fetching snippet: {e}>")
    tree_summ = "\n".join([f"- {f['path']} ({f['ext']}, {f['size_kb']} KB)" for f in flattened[:60]])
    # print("tree_summ variable contains: ", tree_summ)
    prompt = f"""
                You are an expert software architect. 
                Below is a summary of a GitHub repository structure and small snippets from key files.

                ### File Structure (first 60 files):
                {tree_summ}

                ### Key File Headers:
                {headers if headers else 'No key files found.'}

                Please describe in 5–8 sentences:
                1. The overall purpose of this repository.
                2. The main components or modules and their likely roles.
                3. How these modules might interact logically (e.g., data → model → evaluation).
                4. Which parts appear to be core, supporting, or documentation.
                """
    system_msg = SystemMessage(
                content= """
                You are an expert github repository summarizer 
                and provide insights on what functions and modules
                are present in the repository and how they are connected
                to each other. Helping fellow user in understanding 
                the repository basically in leymann terms if possible.
                            """)
    human_msg = HumanMessage(content = prompt)

    llm = state.get("llm")

    response = await llm.ainvoke([system_msg, human_msg])
    global_summ = response.content.strip()

    print("||| Global Context Summary created successfully |||")
    return {**state, "global_context": global_summ}