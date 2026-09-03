import logging
import time
from typing import Any

from app.core.exceptions import (
    NexusException,
    ToolExecutionError,
)

from app.tools.registry import (
    ToolRegistry,
)


logger = logging.getLogger(__name__)


class ToolExecutor:

    def __init__(
        self,
        registry: ToolRegistry,
    ):
        self.registry = registry

    def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        request_id: str | None = None,
    ) -> dict:

        start_time = time.perf_counter()

        logger.info(
            "tool_call_started "
            "request_id=%s "
            "tool_name=%s",
            request_id,
            tool_name,
        )

        try:

            tool = self.registry.get(
                tool_name
            )

            result = tool.execute(
                arguments
            )

            latency_ms = (
                time.perf_counter()
                - start_time
            ) * 1000

            logger.info(
                "tool_call_completed "
                "request_id=%s "
                "tool_name=%s "
                "latency_ms=%.2f "
                "success=True",
                request_id,
                tool_name,
                latency_ms,
            )

            return {
                "success": True,
                "tool_name": tool_name,
                "result": result,
            }

        except NexusException:

            latency_ms = (
                time.perf_counter()
                - start_time
            ) * 1000

            logger.warning(
                "tool_call_failed "
                "request_id=%s "
                "tool_name=%s "
                "latency_ms=%.2f",
                request_id,
                tool_name,
                latency_ms,
            )

            raise

        except Exception as error:

            latency_ms = (
                time.perf_counter()
                - start_time
            ) * 1000

            logger.exception(
                "tool_call_failed "
                "request_id=%s "
                "tool_name=%s "
                "latency_ms=%.2f",
                request_id,
                tool_name,
                latency_ms,
            )

            raise ToolExecutionError(
                tool_name=tool_name,
                message=str(error),
            ) from error