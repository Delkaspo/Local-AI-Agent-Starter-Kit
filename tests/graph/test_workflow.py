from unittest.mock import patch

from langchain_core.messages import AIMessage

from src.graph.workflow import create_workflow, run_workflow


def test_create_workflow():
    """Test the creation of the workflow."""
    workflow = create_workflow()
    assert "graph" in workflow
    assert workflow["graph"] is not None


@patch("src.graph.workflow.BasicToolNode.__call__", return_value={"messages": []})
@patch(
    "src.graph.workflow.ChatbotNode.__call__",
    return_value={"messages": [AIMessage(content="Paris")]},
)
def test_run_workflow(mock_chatbot_node, mock_tool_node):
    """Test running the workflow with a sample query."""

    query = "What is the capital of France?"
    result = run_workflow(query)

    assert "response" in result
    assert result["response"] is not None
    assert "Paris" in result["response"]
    assert mock_chatbot_node.call_count == 1
    assert mock_tool_node.call_count == 0


@patch(
    "src.graph.workflow.BasicToolNode.__call__",
    return_value={"messages": [AIMessage(content="Sunny")]},
)
@patch(
    "src.graph.workflow.ChatbotNode.__call__",
    return_value={
        "messages": [
            AIMessage(
                content="Sunny",
                tool_calls=[
                    {"name": "get_weather", "id": "id", "args": {"city": "Lisbon"}}
                ],
            )
        ]
    },
)
def test_run_workflow_with_tool_call(mock_chatbot_node, mock_tool_node):
    """Test running the workflow with a sample query."""

    query = "What is the weather in Lisbon?"
    result = run_workflow(query)

    assert "response" in result
    assert result["response"] is not None
    assert "Sunny" in result["response"]
    assert (
        mock_chatbot_node.call_count == 2
    )  # 1 for the initial message, 1 for the tool call
    assert mock_tool_node.call_count == 1
