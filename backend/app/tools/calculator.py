from typing import Any

from app.core.exceptions import (
    InvalidToolArgumentsError,
)

from app.tools.base import Tool


class CalculatorTool(Tool):

    name = "calculator"

    description = (
        "Perform basic arithmetic operations "
        "on two numbers."
    )

    @property
    def input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": [
                        "add",
                        "subtract",
                        "multiply",
                        "divide",
                    ],
                    "description": (
                        "The arithmetic operation "
                        "to perform."
                    ),
                },
                "a": {
                    "type": "number",
                    "description": "First number.",
                },
                "b": {
                    "type": "number",
                    "description": "Second number.",
                },
            },
            "required": [
                "operation",
                "a",
                "b",
            ],
        }

    def execute(
        self,
        arguments: dict[str, Any],
    ) -> dict:

        operation = arguments.get("operation")
        a = arguments.get("a")
        b = arguments.get("b")

        if operation not in {
            "add",
            "subtract",
            "multiply",
            "divide",
        }:
            raise InvalidToolArgumentsError(
                tool_name=self.name,
                message="Unsupported operation",
            )

        if not isinstance(
            a,
            (int, float),
        ):
            raise InvalidToolArgumentsError(
                tool_name=self.name,
                message="'a' must be a number",
            )

        if not isinstance(
            b,
            (int, float),
        ):
            raise InvalidToolArgumentsError(
                tool_name=self.name,
                message="'b' must be a number",
            )

        if (
            operation == "divide"
            and b == 0
        ):
            raise InvalidToolArgumentsError(
                tool_name=self.name,
                message="Cannot divide by zero",
            )

        if operation == "add":
            result = a + b

        elif operation == "subtract":
            result = a - b

        elif operation == "multiply":
            result = a * b

        else:
            result = a / b

        return {
            "operation": operation,
            "a": a,
            "b": b,
            "result": result,
        }