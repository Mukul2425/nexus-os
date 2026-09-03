from app.tools.calculator import (
    CalculatorTool,
)

from app.tools.registry import (
    ToolRegistry,
)

from app.tools.time import (
    TimeTool,
)


def create_tool_registry() -> ToolRegistry:

    registry = ToolRegistry()

    registry.register(
        CalculatorTool()
    )

    registry.register(
        TimeTool()
    )

    return registry