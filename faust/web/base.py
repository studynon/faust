"""Base interface for Web server and views."""
from typing import Any, Callable, MutableMapping
from mode import Service
from yarl import URL
from ..cli._env import WEB_BIND, WEB_PORT
from ..types import AppT

__all__ = ['Request', 'Response', 'Web']

_bytes = bytes


class Response:
    """Web server response and status."""


class Web(Service):
    """Web server and HTTP interface."""

    app: AppT

    bind: str
    port: int

    driver_version: str

    def __init__(self, app: AppT,
                 *,
                 port: int = None,
                 bind: str = None,
                 **kwargs: Any) -> None:
        self.app = app
        self.port = port or WEB_PORT
        self.bind = bind or WEB_BIND
        super().__init__(**kwargs)

    def text(self, value: str,
             *,
             content_type: str = None,
             status: int = 200) -> Response:
        ...

    def html(self, value: str,
             *,
             status: int = 200) -> Response:
        ...

    def json(self, value: Any,
             *,
             status: int = 200) -> Response:
        ...

    def bytes(self, value: _bytes,
              *,
              content_type: str = None,
              status: int = 200) -> Response:
        ...

    def route(self, pattern: str, handler: Callable) -> None:
        ...

    def notfound(self, reason: str = 'Not Found', **kwargs: Any) -> Response:
        return self.error(404, reason, **kwargs)

    def error(self, status: int, reason: str, **kwargs: Any) -> Response:
        return self.json({'error': reason, **kwargs}, status=status)

    @property
    def url(self) -> URL:
        return URL(f'http://localhost:{self.port}/')


class Request:
    """HTTP Request."""

    method: str
    url: URL

    @property
    def match_info(self) -> MutableMapping[str, str]:
        ...

    @property
    def query(self) -> MutableMapping[str, str]:
        ...
