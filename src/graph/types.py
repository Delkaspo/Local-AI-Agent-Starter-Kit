from typing import Annotated, List, TypedDict

from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[List[dict], add_messages]
