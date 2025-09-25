import math
from typing import List, TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    values : List[int]
    name : str
    result : str
    operation : str

def operation(state : AgentState) -> AgentState:
    """
    this node performs Multiple operations on a list of integers for a particular individual name. 
    """
    if state['operation'] == '+':
        state['result'] = f"Hello {state['name']}, the total sum of the given items is {sum(state['values'])}"
    # we are using result attribute because we ultimately want our action's ouput to be stored inside the result value.
    elif state['operation'] =='*':
        state['result'] = f"Hello {state['name']}, the total product of the given items is {math.prod(state['values'])}"
    else:
        state['result'] = 'Invalid Operation---'
    return state

graph = StateGraph(AgentState)

graph.add_node("calculator", operation)

graph.set_entry_point("calculator")
graph.set_finish_point("calculator")

app = graph.compile()

answer = app.invoke({'values': [1,2,3,4,5], 'name': 'John Keaton', 'operation': '/'})

print(answer, '\n')
print(answer['result'])