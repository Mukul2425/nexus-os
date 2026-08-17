import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware

from app.logging.context import (
    set_request_id,
)

from app.logging.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request,
        call_next,
    ):

        request_id = str(uuid.uuid4())

        set_request_id(request_id)

        start = time.perf_counter()

        response = await call_next(request)

        latency = (
            time.perf_counter() - start
        )

        logger.info(
            (
                "request_id=%s "
                "method=%s "
                "path=%s "
                "status=%s "
                "latency=%.3fs"
            ),
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            latency,
        )

        response.headers[
            "X-Request-ID"
        ] = request_id

        return response