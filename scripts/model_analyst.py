"""
Script for creating a Repository Analyser Agent
"""
import asyncio
import requests
import base64
import json
from typing import Annotated, Sequence, TypedDict, Union

from dotenv import load_dotenv
from github_repo_parser import GitRepoParser

from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.tools import tool
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage

#loading env variables
load_dotenv()

def flatten_tree(tree, parent_path=""):
     # print("repo_tree variable in flatten_tree function, ", tree)
          files = []
          for key, val in tree.items():
               if isinstance(val, dict) and "type" not in val:
                    files.extend(flatten_tree(val, parent_path + key))
               elif isinstance(val, dict) and val.get("type") == "file":
                    files.append({**val, "folder": parent_path})
               # elif val:
               #      print("val", val)
          return files
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
               headers.append(f"{file_meta["path"]}:\n{snippet}\n")
          except Exception as e:
               headers.append(f"{file_meta["path"]}: <Error in fetching snippet: {e}>")
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

     response = await llm.ainvoke([system_msg, human_msg])
     global_summ = response.content.strip()

     print("||| Global Context Summary created successfully |||")
     return {**state, "global_context": global_summ}

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
