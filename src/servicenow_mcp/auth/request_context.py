from contextvars import ContextVar
from contextlib import contextmanager
from typing import Iterator, Optional

_forwarded_auth_header: ContextVar[Optional[str]] = ContextVar(
    "forwarded_auth_header", default=None
)


def get_forwarded_auth_header() -> Optional[str]:
    return _forwarded_auth_header.get()


@contextmanager
def forwarded_auth_header(header_value: Optional[str]) -> Iterator[None]:
    token = _forwarded_auth_header.set(header_value)
    try:
        yield
    finally:
        _forwarded_auth_header.reset(token)
