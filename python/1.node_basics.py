from operator import add
from typing import Annotated, Literal, TypedDict
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

class State(TypedDict):
    nlist: list[str]


def node_a(state: State) -> State:
    print(f"Node a is receiving State : {state} and nlist : {state["nlist"]}")
    note = "Adding this information from node a"
    return (State(nlist = [note]))

def node_b(state: State) -> State:
    print(f"Node b is receiving State : {state} and nlist : {state["nlist"]}")
    note = "Adding this information from node b"
    return (State(nlist = [note]))

def node_c(state: State) -> State:
    print(f"Node c is receiving State : {state} and nlist : {state["nlist"]}")
    note = "Adding this information from node c"
    return (State(nlist = [note]))


builder = StateGraph(State)

# Adding nodes
# node_a overrides the State and other nodes update to the State.
builder.add_node("a", node_a)
builder.add_node("b", node_b)
builder.add_node("c", node_c)

# Defining the flow

builder.add_edge(START, "a")
builder.add_edge("a", "b")
builder.add_edge("b", "c")
builder.add_edge("c", END)

graph = builder.compile()

initial_state = State(nlist = ["Hello Node, how are you ..?"])

state = graph.invoke(initial_state)

print(state)

