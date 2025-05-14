from unittest.mock import MagicMock, patch

import pytest

from src.tools.web_search import WebSearchTool


@pytest.fixture
def web_search_tool():
    """Fixture for WebSearchTool."""
    tool = WebSearchTool()
    tool.search = MagicMock()
    return tool


@pytest.fixture
def mock_search():
    """Create a mock search wrapper."""
    mock = MagicMock()
    mock.results = MagicMock()
    return mock


@pytest.fixture
def mock_search_results():
    """Fixture for mock search results."""
    return [
        {
            "title": "Test Title 1",
            "snippet": "Test Description 1",
            "link": "https://test1.com",
        },
        {
            "title": "Test Title 2",
            "snippet": "Test Description 2",
            "link": "https://test2.com",
        },
    ]


def test_web_search_tool_initialization(web_search_tool):
    """Test WebSearchTool initialization."""
    assert web_search_tool.name == "web_search"
    assert (
        web_search_tool.description
        == "Search the web for information about a topic. Input should be a search query."
    )


def test_web_search_tool_run_success(web_search_tool, mock_search_results):
    """Test WebSearchTool run method with successful results."""
    web_search_tool.search.results.return_value = mock_search_results
    result = web_search_tool._run("test query")

    expected = """<results>
  <result>
    <title>Test Title 1</title>
    <description>Test Description 1</description>
    <link>https://test1.com</link>
  </result>
  <result>
    <title>Test Title 2</title>
    <description>Test Description 2</description>
    <link>https://test2.com</link>
  </result>
</results>"""
    assert result == expected


def test_web_search_tool_run_no_results(web_search_tool):
    """Test WebSearchTool run method with no results."""
    web_search_tool.search.results.return_value = []
    result = web_search_tool._run("test query")

    assert result == "<results><error>No results found.</error></results>"


def test_web_search_tool_run_error(web_search_tool):
    """Test WebSearchTool run method with error."""
    web_search_tool.search.results.side_effect = Exception("Test error")
    result = web_search_tool._run("test query")

    assert (
        result
        == "<results><error>Error performing web search: Test error</error></results>"
    )
