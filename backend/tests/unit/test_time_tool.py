import pytest

from app.core.exceptions import (
    InvalidToolArgumentsError,
)

from app.tools.time import (
    TimeTool,
)


def test_time_tool():

    tool = TimeTool()

    result = tool.execute(
        {
            "timezone": (
                "Asia/Kolkata"
            )
        }
    )

    assert (
        result["timezone"]
        == "Asia/Kolkata"
    )

    assert "datetime" in result


def test_invalid_timezone():

    tool = TimeTool()

    with pytest.raises(
        InvalidToolArgumentsError
    ):
        tool.execute(
            {
                "timezone": (
                    "Invalid/Timezone"
                )
            }
        )


def test_missing_timezone():

    tool = TimeTool()

    with pytest.raises(
        InvalidToolArgumentsError
    ):
        tool.execute({})