from datetime import datetime
from zoneinfo import ZoneInfo

from app.core.exceptions import (
    InvalidToolArgumentsError,
)

from app.tools.base import Tool


class TimeTool(Tool):

    name = "time"

    description = (
        "Get the current date and time "
        "for a valid IANA timezone."
    )

    @property
    def input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "timezone": {
                    "type": "string",
                    "description": (
                        "An IANA timezone, for example "
                        "'Asia/Kolkata' or 'America/New_York'."
                    ),
                },
            },
            "required": [
                "timezone",
            ],
        }

    def execute(
        self,
        arguments: dict,
    ) -> dict:

        timezone = arguments.get(
            "timezone"
        )

        if not isinstance(
            timezone,
            str,
        ):
            raise InvalidToolArgumentsError(
                tool_name=self.name,
                message=(
                    "'timezone' must be a string"
                ),
            )

        try:
            zone = ZoneInfo(timezone)

        except Exception as error:

            raise InvalidToolArgumentsError(
                tool_name=self.name,
                message=(
                    f"Invalid timezone: {timezone}"
                ),
            ) from error

        current_time = datetime.now(
            zone
        )

        return {
            "timezone": timezone,
            "datetime": (
                current_time.isoformat()
            ),
        }