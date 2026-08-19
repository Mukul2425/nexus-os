from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import NexusException
from app.logging.context import get_request_id
from app.logging.logger import logger


async def nexus_exception_handler(
    request: Request,
    exc: NexusException,
):

    request_id = get_request_id()

    logger.error(
        "application_error "
        "request_id=%s "
        "code=%s "
        "message=%s",
        request_id,
        exc.code,
        exc.message,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "request_id": request_id,
            }
        },
    )