from app.tools.factory import (
    create_tool_registry,
)


def test_default_tools_registered():

    registry = create_tool_registry()

    assert registry.has(
        "calculator"
    )

    assert registry.has(
        "time"
    )


def test_tool_definitions():

    registry = create_tool_registry()

    definitions = registry.get_definitions()

    names = {
        tool.name
        for tool in definitions
    }

    assert "calculator" in names
    assert "time" in names