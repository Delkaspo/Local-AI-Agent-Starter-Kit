from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import BaseTool
from langchain_ollama import ChatOllama

from config.settings import settings
from graph.types import State
from tools import tools


class ChatbotNode:
    def __init__(self):
        self.llm = ChatOllama(model=settings.OLLAMA_MODEL, temperature=0.7).bind_tools(
            tools
        )

    def __call__(self, state: State) -> State:
        messages = [
            SystemMessage(
                content="You are a helpful AI assistant. Use the tools available to help answer the user's questions."
            )
        ] + state["messages"]

        response = self.llm.invoke(messages)

        return {
            "messages": [response],
        }
