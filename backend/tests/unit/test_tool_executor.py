import pytest

from app.core.exceptions import (
    UnknownToolError,
)

from app.tools import (
    create_tool_registry,
)

from app.tools.executor import (
    ToolExecutor,
)


def test_execute_calculator():

    registry = (
        create_tool_registry()
    )

    executor = ToolExecutor(
        registry
    )

    response = executor.execute(
        tool_name="calculator",
        arguments={
            "operation": "add",
            "a": 10,
            "b": 20,
        },
        request_id="test-request",
    )

    assert response["success"] is True

    assert (
        response["result"]["result"]
        == 30
    )


def test_unknown_tool():

    registry = (
        create_tool_registry()
    )

    executor = ToolExecutor(
        registry
    )

    with pytest.raises(
        UnknownToolError
    ):
        executor.execute(
            tool_name="unknown",
            arguments={},
        )