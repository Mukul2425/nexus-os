from app.core.exceptions import (
    UnknownToolError,
)

from app.tools.base import Tool
from app.schemas.llm import ToolDefinition

class ToolRegistry:

    def __init__(self):
        self._tools: dict[
            str,
            Tool,
        ] = {}

    def register(
        self,
        tool: Tool,
    ) -> None:

        self._tools[tool.name] = tool

    def get(
        self,
        tool_name: str,
    ) -> Tool:

        tool = self._tools.get(
            tool_name
        )

        if tool is None:
            raise UnknownToolError(
                tool_name
            )

        return tool

    def has(
        self,
        tool_name: str,
    ) -> bool:

        return (
            tool_name in self._tools
        )

    def list_tools(
        self,
    ) -> list[Tool]:

        return list(
            self._tools.values()
        )


    def get_definitions(
        self,
    ) -> list[ToolDefinition]:

        return [
            ToolDefinition(
                name=tool.name,
                description=tool.description,
                input_schema=tool.input_schema,
            )
            for tool in self.list_tools()
        ]