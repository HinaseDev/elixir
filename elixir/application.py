"""
Minimalist WSGI-App Server
"""

from typing import Any, Union
from elixir.request import Request
from elixir.middleware import Headers, HeaderSet, InitialHeaders

class WSGI:
    """
    Most basic Handler for WSGI Servers.

    Sample Usage:

    ```py
    from elixir.application import WSGI, wrap_response
    from elixir.serving import run_server

    def recv(request, response):
        return wrap_response("Hello World", response)

    run_server(WSGI(recv))
    ```
    """
    def __init__(self, handler) -> None:
        """
        Instanciates a new class of type :WSGI:
        """
        self.wrapped_app = handler

    def __call__(self, environ, start_response, *args: Any, **kwds: Any) -> Any:
        return self.wrapped_app(Request(environ), start_response)

def wrap_response(text, start_response, *, headers: Headers=InitialHeaders, status_code="200 Ok", mimetype="text/html"):
    """
    Creates a WSGI-Style Response
    """
    headers["Content-Type"] = mimetype
    if isinstance(text, str):
        body = text.encode("utf-8")


    start_response(status_code, headers.as_wsgi)
    return [body]
