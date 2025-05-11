from datetime import datetime
from typing import Optional, Type

from langchain_core.tools import BaseTool


class DateTimeTool(BaseTool):
    """Tool for getting current date and time."""

    name: str = "get_current_time"
    description: str = "Get the current date and time."
    args_schema: Optional[Type] = None

    def _run(self, _: str = "") -> str:
        now = datetime.now()
        return now.strftime("The current date is %Y-%m-%d and the time is %H:%M:%S.")
