# langgraph_app.py

from langgraph.graph import StateGraph, END
from scripts.repo_parser.state_schema import Agent_State

# --- Import all nodes ---
from scripts.repo_parser.nodes.fetch_repo_metadata_node import fetch_repo_metadata_node
from scripts.repo_parser.nodes.global_context_node import global_context_node
from scripts.repo_parser.nodes.analyze_repo_node import analyze_tree_node
from scripts.repo_parser.nodes.fetch_and_parse_node import fetch_and_parse_node
from scripts.repo_parser.nodes.summarize_repo_node import summarize_repo_node

workflow = StateGraph(Agent_State)

# Register nodes
workflow.add_node("fetch_metadata", fetch_repo_metadata_node)
workflow.add_node("global_context", global_context_node)
workflow.add_node("analyze_tree", analyze_tree_node)
workflow.add_node("fetch_and_parse", fetch_and_parse_node)
workflow.add_node("summarize", summarize_repo_node)

# Define workflow edges
workflow.add_edge("fetch_metadata", "global_context")
workflow.add_edge("global_context", "analyze_tree")
workflow.add_edge("analyze_tree", "fetch_and_parse")
workflow.add_edge("fetch_and_parse", "summarize")
workflow.add_edge("summarize", END)

# Define entry node
workflow.set_entry_point("fetch_metadata")

# Compile the workflow into an app instance
app = workflow.compile()

__all__ = ["app"]
