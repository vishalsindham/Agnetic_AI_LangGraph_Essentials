import operator
from typing import Annotated, List, Literal, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


class State(TypedDict):
    nlist: Annotated[list[str], operator.add]


# def node_a(state: State) -> State:
#     return


def node_b(state: State) -> State:
    return State(nlist=["B"])


def node_c(state: State) -> State:
    return State(nlist=["C"])


# We can define the control flow of the graph. Where based on the state of the graph we decide
# where the control will flow and data will be processed.
# One way is to define the function we can write the required business logic.


def conditional_edge(state: State) -> Literal["b", "c", END]:
    select = state["nlist"][-1]
    if select == "b":
        return "b"
    elif select == "c":
        return "c"
    elif select == "q":
        return END
    else:
        return END


# Second way is to write using the Command scheme type. We define the logic of routing inside
# node itself using the Command class.


def node_a(state: State) -> Command[Literal["b", "c", END]]:
    select = state["nlist"][-1]
    if select == "b":
        next_node = "b"
    elif select == "c":
        next_node = "c"
    elif select == "q":
        next_node = "q"
    else:
        next_node = END
    return Command(update=State(nlist=[f"Enduser input : {select}"]), goto=[next_node])


builder = StateGraph(State)

# Add nodes
builder.add_node("a", node_a)
builder.add_node("b", node_b)
builder.add_node("c", node_c)

# Add edges
builder.add_edge(START, "a")
# builder.add_conditional_edges("a", conditional_edge)
builder.add_edge("b", END)
builder.add_edge("c", END)
graph = builder.compile()

# graph.get_graph().draw_mermaid_png(output_file_path="conditional_edges_with_command.png")
while True:
    user = input("b, c, or q to quit: ")
    input_state = State(nlist=[user])
    response = graph.invoke(input_state)
    print(response)
    if "q" in response["nlist"][-1]:
        print("quit")
        break
