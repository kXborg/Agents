from typing import List, TypedDict
from langgraph.graph import StateGraph


class AgentState(TypedDict):
    name: str
    age: int
    skills: List
    output: str


def first_node(state: AgentState) -> AgentState:
    """
    This is the first node. It personalizes the name field with a greeting
    """

    state['output'] = f"Hey, {state['name']} welcome to the system!!"

    return state

def second_node(state: AgentState) -> AgentState:
    """
    This is te second node. It describes the age of the user.
    """

    state['output'] = state['output'] + f"You are {state['age']} years old."

    return state

def third_node(state: AgentState) -> AgentState:
    """
    This is the third node. It lists the user's skills in a formatted string.
    """

    state['output'] = state['output'] + f" You have skills in: {", ".join(state['skills'])}."

    return state

graph = StateGraph(AgentState)

graph.add_node('first_node', first_node)
graph.add_node('second_node', second_node)
graph.add_node('third_node', third_node)

graph.set_entry_point('first_node')
graph.add_edge('first_node', 'second_node')
graph.add_edge('second_node', 'third_node')
graph.set_finish_point('third_node')

app = graph.compile()

answer = app.invoke({'name': 'John Keaton', 'age': '34', 'skills': ['genAI', 'pytorch', 'agenticDiffusion']})

print(answer['output'])