from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.tools import BaseTool
from pydantic import Field


class WebSearchTool(BaseTool):
    """Tool for performing web searches using DuckDuckGo."""

    name: str = "web_search"
    description: str = (
        "Search the web for information about a topic. Input should be a search query."
    )
    search: DuckDuckGoSearchAPIWrapper = Field(
        default_factory=DuckDuckGoSearchAPIWrapper
    )

    def _run(self, query: str) -> str:
        """Run the web search tool.

        Args:
            query: The search query to look up.

        Returns:
            A string containing the search results in XML format.
        """
        try:
            results = self.search.results(query, max_results=3)
            if not results:
                return "<results><error>No results found.</error></results>"

            formatted_results = ["<results>"]
            for result in results:
                title = result.get("title", "No title")
                snippet = result.get("snippet", "No description")
                link = result.get("link", "No link")
                formatted_results.append(
                    f"""  <result>
    <title>{title}</title>
    <description>{snippet}</description>
    <link>{link}</link>
  </result>"""
                )
            formatted_results.append("</results>")
            return "\n".join(formatted_results)
        except Exception as e:
            return f"<results><error>Error performing web search: {str(e)}</error></results>"
