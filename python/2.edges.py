import operator
from typing import Annotated, Literal, TypedDict
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

class State(TypedDict):
    nlist: Annotated[list[str], operator.add]

# Defining nodes

def node_a(state: State) -> State:
    print(f"Entering node a with state : {state}")
    print(f"Adding 'A' to {state['nlist']}")
    return (State(nlist = ["A"]))

def node_b(state: State) -> State:
    print(f"Entering node b with state : {state}")
    print(f"Adding 'B' to {state['nlist']}")
    return (State(nlist = ["B"]))

def node_c(state: State) -> State:
    print(f"Entering node c with state : {state}")
    print(f"Adding 'C' to {state['nlist']}")
    return (State(nlist = ["C"]))

def node_bb(state: State) -> State:
    print(f"Entering node bb with state : {state}")
    print(f"Adding 'BB' to {state['nlist']}")
    return (State(nlist = ["BB"]))

def node_cc(state: State) -> State:
    print(f"Entering node cc with state : {state}")
    print(f"Adding 'cc' to {state['nlist']}")
    return (State(nlist = ["CC"]))

def node_d(state: State) -> State:
    print(f"Entering node d with state : {state}")
    print(f"Adding 'd' to {state['nlist']}")
    return (State(nlist = ["D"]))

# Building the graph
# Adding the nodes to the graph
builder = StateGraph(State)
builder.add_node("a", node_a)
builder.add_node("b", node_b)
builder.add_node("c", node_c)
builder.add_node("cc",node_cc)
builder.add_node("bb", node_bb)
builder.add_node("d", node_d)


# Defining the flow of the graph
builder.add_edge(START, "a")
builder.add_edge("a", "b")
builder.add_edge("a", "c")
builder.add_edge("b","bb")
builder.add_edge("c", "cc")
builder.add_edge("bb", "d")
builder.add_edge("cc", "d")
builder.add_edge("d", END)

# Above we only defined the graph, if we don't compile we can't use it.
graph = builder.compile()

# Initial state we defined.
initial_state = State(
    nlist = ["Initial String: "]
)

response = graph.invoke(initial_state)

# Invoked graph returns the final state of the passed state.
print(response)