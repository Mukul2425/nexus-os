import pytest

from app.core.exceptions import (
    InvalidToolArgumentsError,
)

from app.tools.calculator import (
    CalculatorTool,
)


def test_add():

    tool = CalculatorTool()

    result = tool.execute(
        {
            "operation": "add",
            "a": 10,
            "b": 20,
        }
    )

    assert result["result"] == 30


def test_subtract():

    tool = CalculatorTool()

    result = tool.execute(
        {
            "operation": "subtract",
            "a": 20,
            "b": 5,
        }
    )

    assert result["result"] == 15


def test_multiply():

    tool = CalculatorTool()

    result = tool.execute(
        {
            "operation": "multiply",
            "a": 10,
            "b": 5,
        }
    )

    assert result["result"] == 50


def test_divide():

    tool = CalculatorTool()

    result = tool.execute(
        {
            "operation": "divide",
            "a": 20,
            "b": 4,
        }
    )

    assert result["result"] == 5


def test_divide_by_zero():

    tool = CalculatorTool()

    with pytest.raises(
        InvalidToolArgumentsError
    ):
        tool.execute(
            {
                "operation": "divide",
                "a": 10,
                "b": 0,
            }
        )


def test_invalid_operation():

    tool = CalculatorTool()

    with pytest.raises(
        InvalidToolArgumentsError
    ):
        tool.execute(
            {
                "operation": "power",
                "a": 2,
                "b": 3,
            }
        )


def test_invalid_number():

    tool = CalculatorTool()

    with pytest.raises(
        InvalidToolArgumentsError
    ):
        tool.execute(
            {
                "operation": "add",
                "a": "ten",
                "b": 20,
            }
        )