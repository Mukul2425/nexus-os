from app.tools.calculator import CalculatorTool
from app.tools.executor import ToolExecutor
from app.tools.registry import ToolRegistry
from app.tools.time import TimeTool


def create_tool_registry() -> ToolRegistry:

    registry = ToolRegistry()

    registry.register(
        CalculatorTool()
    )

    registry.register(
        TimeTool()
    )

    return registry


def create_tool_executor() -> ToolExecutor:

    registry = create_tool_registry()

    return ToolExecutor(
        registry
    )