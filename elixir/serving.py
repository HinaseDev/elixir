from wsgiref.simple_server import make_server as _ex_make_server
from elixir.application import WSGI, Headers, Request
from typing import Any, List, ByteString

def make_empty_environment():
    return {
        "REQUEST_METHOD": "GET",
        "PATH_INFO":"/",
        "QUERY_STRING": "",
        "SERVER_PORT": 5000,
        "SERVER_PROTOCOL": "HTTP/1.1",
        "SERVER_NAME": "localhost"
    }

def fake_start_response(s, h):
    ...

def check_app(app):
    """
    Called by make_server() to assert that the WSGI App is capable of working
    with WSGI Environments.

    >>> from my_server import app
    >>> check_app(app)
    True
    >>> check_app("This wont work")
    False

    Essentially, this function creates a sample WSGI Environment and passes it to the app
    """
    if isinstance(app, WSGI): # Standard WSGI App, will always pass
        return True
    env = make_empty_environment()
    result = app(Request(env), fake_start_response)
    return isinstance(result, list) and all([isinstance(line, bytes) for line in result] )
    

def make_server(host: str, port: int, app: Any, skip_test=True):
    if not skip_test:
        assert check_app(app)
    return _ex_make_server(host, port, app)

def run_server(app, host="localhost", port=1234):
    server = make_server(host, port, app)
    server.serve_forever()
