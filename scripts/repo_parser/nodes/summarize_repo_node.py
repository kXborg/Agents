# nodes/summarize_repo_node.py
from scripts.repo_parser.config.settings import MAX_CHUNKS, LLM

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

async def summarize_repo_node(state: dict) -> dict:
    """
    Final summarization node.
    Combines global context + parsed files + user query
    into a multi-chat answer.
    """

    print("Initializing Summarize Repo Node...") 

    llm = state.get("llm")
    if not llm:
        return {**state, "messages": state.get("messages", []) + [
            SystemMessage(content="LLM not found in state, cannot summarize.")
        ]}

    user_query = ""
    for msg in reversed(state.get("messages", [])):
        if isinstance(msg, HumanMessage):
            user_query = msg.content
            break

    if not user_query:
        user_query = "Provide a summary of this repository."

    global_overview = state.get("global_context", "")
    parsed_files = state.get("parsed_files", [])

    # Reduce parsed files to a manageable token length
    merged_chunks = []

    for f in parsed_files[:MAX_CHUNKS]:
        merged_chunks.append(
            f"\n### File: {f['path']}\n{f['parsed']}\n"
        )

    merged_text = "\n".join(merged_chunks)

    system_msg = SystemMessage(content="""
You are an expert software engineer.
Your job is to analyze and explain source code repositories clearly, 
logically, and accurately. 
You must always:
- reflect the structure of the repository,
- integrate global context with file-level details,
- and answer the user's query precisely.
""")

    human_msg = HumanMessage(content=f"""
User Query:
{user_query}

Global Repository Context:
{global_overview}

Relevant Parsed Files:
{merged_text}

Now produce a clear, structured response addressing the user's question.
""")
    # llm = state.get("llm")
    llm = LLM
    response = await llm.ainvoke([system_msg, human_msg])
    # print(f"Response Variable: {response}")
    new_ai_msg = AIMessage(content=response.content)

    return {
        **state,
        "summary": response.content,
        "messages": state.get("messages", []) + [new_ai_msg],
    }
