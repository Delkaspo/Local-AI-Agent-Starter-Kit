from typing import Any, Dict

from langchain_core.messages import HumanMessage
from langgraph.graph import END, START, StateGraph

from .nodes.chatbot import ChatbotNode
from .nodes.tools import BasicToolNode
from .types import State


def create_workflow() -> Dict[str, Any]:
    """Create and initialize the workflow agent."""
    workflow = StateGraph(State)

    chatbot_node = ChatbotNode()
    tool_node = BasicToolNode()
    workflow.add_node("chatbot", chatbot_node)
    workflow.add_node("tools", tool_node)

    workflow.add_edge(START, "chatbot")
    workflow.add_edge("tools", "chatbot")

    def route_tools(
        state: State,
    ):
        """
        Use in the conditional_edge to route to the ToolNode if the last message
        has tool calls. Otherwise, route to the end.
        """
        if isinstance(state, list):
            ai_message = state[-1]
        elif messages := state.get("messages", []):
            ai_message = messages[-1]
        else:
            raise ValueError(f"No messages found in input state to tool_edge: {state}")
        if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
            return "tools"
        return END

    workflow.add_conditional_edges(
        "chatbot",
        route_tools,
        {"tools": "tools", END: END},
    )
    return {"graph": workflow.compile()}


def run_workflow(query: str) -> Dict[str, Any]:
    agent = create_workflow()
    state = {"messages": [HumanMessage(content=query)]}
    result = agent["graph"].invoke(state)
    last_message = result["messages"][-1]
    return {"response": last_message.content}
