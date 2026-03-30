from typing import Dict, TypedDict
from langgraph.graph import StateGraph


# we will start with creating the state of the agent: 
# A shared datastructure that keeps track of information, let's call it AgentState

class AgentState(TypedDict):
    #creating a very simple input 
    message : str

def complimentor(state: AgentState) -> AgentState:
    # we need to write a doc-string in this function that tells the node what function it needs to perform
    """
    Adds a compliment message to the input string.
    """
    # now we need to access the message contained in the current state variable, a simple python.

    state['message'] = "Hello " + state['message'] + ", you are doing an amazing job in learning langGraph!!"

    return state

graph = StateGraph(AgentState)

# first parameter in the below line of code is the name of our main single node
graph.add_node("appreciator", action = complimentor)

# setting the starting and ending nodes
graph.set_entry_point("appreciator")
graph.set_finish_point("appreciator")

app = graph.compile()

# the input to the invoke method is a TypedDict because that's how we defined our state.
result = app.invoke({'message': "John Keaton"})

print(result["message"])

