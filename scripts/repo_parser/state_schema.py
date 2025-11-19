# state_schema.py

from typing import Annotated, Sequence, TypedDict, Union, Dict, List
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from scripts.repo_parser.config.settings import LLM


class Agent_State(TypedDict):
    """
    LangGraph state structure for the Repo Analyzer + Summarizer Agent.
    
    This is the central shared memory between all nodes.
    """

    # Conversation memory (multi-chat)
    messages: Annotated[Sequence[BaseMessage], add_messages]

    # GitHub repo input
    url: Union[str, None]

    # Metadata tree returned by GitRepoParser
    repo_tree: Dict[str, any]

    # High-level global context summary
    global_context: Union[str, None]

    # Files selected after query-aware filtering
    selected_files: List[Dict[str, any]]

    # Files skipped due to size/type
    skipped_files: List[str]

    # Parsed file contents (LLM-friendly)
    parsed_files: List[Dict[str, str]]

    # Final summarization or answer from LLM
    summary: Annotated[Sequence[BaseMessage], add_messages]

    # LLM instance injected into state
    llm: LLM
