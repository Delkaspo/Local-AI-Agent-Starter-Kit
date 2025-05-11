from datetime import datetime
from unittest.mock import patch

import pytest

from src.tools.datetime_tool import DateTimeTool


@pytest.fixture
def datetime_tool():
    """Fixture for DateTimeTool."""
    return DateTimeTool()


def test_datetime_tool_initialization(datetime_tool):
    """Test DateTimeTool initialization."""
    assert datetime_tool.name == "get_current_time"
    assert datetime_tool.description == "Get the current date and time."
    assert datetime_tool.args_schema is None


def test_datetime_tool_run(datetime_tool):
    """Test DateTimeTool run method."""
    mock_date = datetime(2024, 3, 15, 12, 30, 45)
    with patch("src.tools.datetime_tool.datetime") as mock_datetime:
        mock_datetime.now.return_value = mock_date
        result = datetime_tool._run()

        expected = "The current date is 2024-03-15 and the time is 12:30:45."
        assert result == expected


def test_datetime_tool_run_with_empty_input(datetime_tool):
    """Test DateTimeTool run method with empty input."""
    mock_date = datetime(2024, 3, 15, 12, 30, 45)
    with patch("src.tools.datetime_tool.datetime") as mock_datetime:
        mock_datetime.now.return_value = mock_date
        result = datetime_tool._run("")

        expected = "The current date is 2024-03-15 and the time is 12:30:45."
        assert result == expected
