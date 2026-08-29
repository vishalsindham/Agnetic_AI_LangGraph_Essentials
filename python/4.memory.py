import operator
from typing import Annotated, List, Literal, TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


class State(TypedDict):
    nlist: Annotated[list["str"], operator.add]


def node_a(state: State) -> Command[Literal["b", "c", END]]:
    select = state["nlist"][-1]
    if select == "b":
        next_node = "b"
    elif select == "c":
        next_node = "c"
    elif select == "q":
        next_node = END
    else:
        next_node = END

    return Command(update=State(nlist=[select]), goto=[next_node])


def node_b(state: State) -> State:
    return (State(nlist=["B"]))


def node_c(state: State) -> State:
    return (State(nlist=["C"]))


builder = StateGraph(State)

# Add nodes
builder.add_node("a", node_a)
builder.add_node("b", node_b)
builder.add_node("c", node_c)

# Add edges
builder.add_edge(START, "a")
builder.add_edge("b", END)
builder.add_edge("c", END)


# graph.get_graph().draw_mermaid_png(output_file_path="memory.png")

memory = InMemorySaver()
config = {"configurable": {"thread_id": "1"}}

graph = builder.compile(checkpointer=memory)

while True:
    user = input("b, c, or q to quit: ")
    input_state = State(nlist=[user])
    result = graph.invoke(input_state, config)
    print(result["nlist"])
    if "q" in result["nlist"][-1]:
        print("quit")
        break
