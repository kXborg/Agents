# run_cli.py

import asyncio
import sys

from scripts.repo_parser.langgraph_app import app
from scripts.repo_parser.config.settings import LLM
from scripts.repo_parser.state_schema import Agent_State


async def run(repo_url: str):
    """
    Execute the LangGraph pipeline on the given repo URL via CLI.
    """

    # Initial state for the graph
    state: Agent_State = {
        "messages": [],
        "url": repo_url,
        "repo_tree": {},
        "global_context": None,
        "selected_files": [],
        "skipped_files": [],
        "parsed_files": [],
        "summary": None,
        "llm": LLM,
    }

    print(f"\nStarting analysis for repo:\n{repo_url}\n")

    async for step in app.astream(state):
        # step is a dict: {"node_name": updated_state}
        node_name = list(step.keys())[0]
        print(f"Node executed: {node_name}")

        # Optionally print the node's output
        updated_state = step[node_name]
        if "messages" in updated_state:
            last_msg = updated_state["messages"][-1]
            print(f"  Message: {last_msg.content if hasattr(last_msg, 'content') else last_msg}")

    print("\nFinished processing repo.\n")
    # print(f"Summary state: {state['summary']}")
    # FINAL OUTPUT
    if state.get("summary"):
        print("FINAL SUMMARY:\n")
        print(state["summary"])
    else:
        print("No summary generated.")


if __name__ == "__main__":
    # Expect repo URL as CLI argument
    if len(sys.argv) < 2:
        print("Usage: python run_cli.py <github_repo_url>")
        sys.exit(1)

    repo_url = sys.argv[1]

    asyncio.run(run(repo_url))
