from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
        number_1: int
        operation_1: str
        number_2: int
        result_1: int
        number_3: int
        operation_2: str
        number_4: int
        result_2: int

def adder_1(state: AgentState) -> AgentState:
    """
    This is the node that do addition operation
    """

    state['result_1'] = state['number_1'] + state['number_2']
    

    return state

def substracter_1(state: AgentState) -> AgentState:
      """
      This is the node that performs substraction operation
      """

      state['result_1'] = state['number_1'] - state['number_2']

      return state

def adder_2(state: AgentState) -> AgentState:
    """
    This is the node that do addition operation
    """

    state['result_2'] = state['number_3'] + state['number_4']
    

    return state

def substracter_2(state: AgentState) -> AgentState:
      """
      This is the node that performs substraction operation
      """

      state['result_2'] = state['number_3'] - state['number_4']

      return state

def first_router(state: AgentState) -> AgentState:
      """
      This is the conditional node or router which decides which edge to traverse on.
      """

      #in the below code, the return strings are the names of the conditional edges which we will be using later on the code.
    
      if state['operation_1'] == '+':
            return 'first_addition_edge'
      else: 
            return 'first_substrator_edge'
def second_router(state: AgentState) -> AgentState:
      """
      This is the function that implements the functionality of the second router
      """
      if state['operation_2'] == '+':
            return 'second_addition_edge'
      else: 
            return 'second_substraction_edge'

      
graph = StateGraph(AgentState)


graph.add_node('addition_node', adder_1)
graph.add_node('substraction_node', substracter_1)
graph.add_node('second_addition_node', adder_2)
graph.add_node('second_substraction_node', substracter_2)


graph.add_node('router_1', lambda state: state) #pass through function, as our router function doesn't have return a state variable, instead it returns a string only
graph.add_node('router_2', lambda state: state)


graph.add_edge(START, 'router_1')


graph.add_conditional_edges(
      'router_1',
      first_router,
      {
            #edge-node relationship
            'first_addition_edge': 'addition_node',
            'first_substractor_edge': 'substraction_node'

      }

)

graph.add_edge('addition_node', 'router_2')
graph.add_edge('substraction_node', 'router_2')

graph.add_conditional_edges(
      'router_2',
      second_router,
      {
            'second_addition_edge': 'second_addition_node',
            'second_substraction_edge': 'second_substraction_node'
      }
)

graph.add_edge('second_addition_node', END)
graph.add_edge('second_substraction_node', END)


agent = graph.compile()

initial_state = AgentState(number_1 = 9, operation_1 ='+', number_2 = 8, number_3 = 7, operation_2 = '-', number_4 = 97, result_1 = 0, result_2 = 0)
# results = agent.invoke({'number_1': 9, 'operation': '+', 'number_2': 8, 'number_3': 7, 'operation_2': '-', 'number_4': 97, 'result_1': 0, 'result_2': 0})
# print('This is the result of the first operation that you provided: ', results['result_1'])
# print('This is the result of the second operation that you wanted to do: ', results['result_2'])
output = agent.invoke(initial_state)
print('This is the result of the first operation: ', output['result_1'])
print('This is the result of the second operation: ', output['result_2'])