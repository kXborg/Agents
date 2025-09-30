import base64, asyncio
from dotenv import load_dotenv
from typing import Annotated, Sequence, List, TypedDict, Union

from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

from langchain_core.tools import tool
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage

from playwright.async_api import async_playwright, Page, Browser

#loading env variables
load_dotenv()

#system prompt
#Remember: Improve System Prompt
system_msg = SystemMessage(
     content= f"""
     You are an expert model analyst working on inferencing latest llm's and vlm's 
     to provide a rough estimate on the model's inference performance. 
"""
)

#Agent State Defination
class agent_state(TypedDict):
     messages: Annotated[Sequence[BaseMessage], add_messages]
     url: str
     error: str
     iterations: int
     explanation: str

