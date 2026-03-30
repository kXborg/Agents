"""
Script for creating a Repository Analyser Agent
"""
import asyncio
import requests
import base64
import json
from typing import Annotated, Sequence, TypedDict, Union

from dotenv import load_dotenv
from scripts.repo_parser.github_repo_parser import GitRepoParser

from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.tools import tool
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage

#loading env variables
load_dotenv()
# class AgentState(TypedDict):
#      """
#      Defining Agent State 
#      """
#      messages: Annotated[Sequence[BaseMessage], add_messages]
#      url: Union[str, None]
#      repo_content: Union[str, None]
#      summary: Annotated[Sequence[BaseMessage], add_messages]

# def set_default(obj):
#      if isinstance(obj, set):
#           return list(obj)
#      raise TypeError

# @tool
# async def fetch_repo(url: str) -> str:
#      """
#      Fetches the content of a github repository from
#      github_repo_parser module.
#      Content is in textual format.
#      """
#      if not url.startswith("https://github.com/"):
#           return "Invalid Github URL format"
     
#      print("-----Initializing Fetch Repo Tool-----")

#      try:
#           grp = GitRepoParser(github_token = True)
#           items = grp.fetch_content(grp.url_parse(url))
#           return json.dumps(items, default= set_default, indent=2)
#      except Exception as e:
#           return f"Error in fetching repo: {e}"
     
# agent_tool = [fetch_repo]
llm = ChatGoogleGenerativeAI(model = 'gemini-2.5-flash')#.bind_tools(tools = agent_tool)



async def analyze_repo_node(state: dict)->dict:
      """
      This 
      """

# async def test_global_context_node():
#      grp = GitRepoParser(github_token=True)
#      repo_tree = grp.get_dir_tree("https://github.com/facebookresearch/dinov2")
#      # print(f"repo_tree variable contains: {repo_tree}")
#      state = {
#           "repo_tree": repo_tree,
#           "llm": llm
#      }
#      new_state = await global_context_node(state)
#      print("\n GLOBAL CONTEXT SUMMARY: \n")
#      print(new_state["global_context"])

# asyncio.run(test_global_context_node())


# async def fetch_repo_node(state: AgentState) -> AgentState:
#      """
#      Node which calls fetch_repo tool and stores
#      output in state.
#      """
#      print("-----Initializing Fetch Repo Node-----")
     
#      repo_data = await fetch_repo.ainvoke(state['url'])

#      return {
#           **state,
#           'repo_content': repo_data,
#           'messages': state["messages"] + [SystemMessage(content=f"Repo fetched Successfully")]
#      }

# #REMEMBER: Token count can be reduced here.
# async def summarize_node(state: AgentState) -> AgentState:
#      """
#      This node analyzes and summarizes 
#      the content fetched from github repository provided. 
#      """

#      print("-----Initializing Summarize Node-----")
#      # repo_content = state.get
#      prompt = HumanMessage(content = f"""Summarize this repository
#                            contents for me in a leyman terms
#                            :\n{state.get('repo_content')}""")
     
#      summary = await llm.ainvoke([system_msg, prompt])
#      print("-----LLM Summarization Successful-----")

#      return {
#           **state,
#           "messages": state["messages"] + [SystemMessage(content="Repo summarization completed.")],
#           "summary": state.get("summary") + [summary]
#      }

# workflow = StateGraph(AgentState)

# workflow.add_node("fetch", fetch_repo_node)
# workflow.add_node("summarize", summarize_node)

# workflow.add_edge(START, "fetch")
# workflow.add_edge("fetch", "summarize")
# workflow.add_edge("summarize", END)

# app = workflow.compile()

# async def main():
     
#      state = {
#           "messages": [],
#           "url":  "https://github.com/bhomik749/vlm-bench",
#           "repo_content": None,
#           "summary": []
#      }
     
#      async for step in app.astream(state):
#           print(step)
# asyncio.run(main())
