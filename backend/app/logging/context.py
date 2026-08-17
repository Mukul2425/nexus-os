from contextvars import ContextVar

_request_id: ContextVar[str] = ContextVar(
    "request_id",
    default="-",
)


def set_request_id(request_id: str):
    _request_id.set(request_id)


def get_request_id() -> str:
    return _request_id.get()