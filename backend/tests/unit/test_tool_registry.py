import pytest

from app.core.exceptions import (
    UnknownToolError,
)

from app.tools.calculator import (
    CalculatorTool,
)

from app.tools.registry import (
    ToolRegistry,
)


def test_register_and_get_tool():

    registry = ToolRegistry()

    tool = CalculatorTool()

    registry.register(tool)

    assert (
        registry.get("calculator")
        is tool
    )


def test_has_tool():

    registry = ToolRegistry()

    registry.register(
        CalculatorTool()
    )

    assert registry.has(
        "calculator"
    )

    assert not registry.has(
        "unknown"
    )


def test_unknown_tool():

    registry = ToolRegistry()

    with pytest.raises(
        UnknownToolError
    ):
        registry.get("unknown")


def test_list_tools():

    registry = ToolRegistry()

    registry.register(
        CalculatorTool()
    )

    tools = registry.list_tools()

    assert len(tools) == 1
    assert (
        tools[0].name
        == "calculator"
    )