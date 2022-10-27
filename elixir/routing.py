from elixir.application import WSGI, Headers, Request
from elixir.serving import check_app
from elixir.helpers import Error
from typing import Any
import re

class RoutableWSGIApp(WSGI):
    def __init__(self, routes) -> None:
        self.map = Map(routes)

    
    def __call__(self, environ, start_response, *args: Any, **kwds: Any) -> Any:
        req = Request(environ)
        rule = self.map.find_rule(req.path)
        return (rule.endpoint)(environ, start_response)
        
        
class Rule:
    def __init__(self, route, endpoint, *, attrgetter: object = None, attrgetter__search="__getattribute__", forceverify=True) -> None:
        self.name = route
        self.endpoint = endpoint
        self.__attrgetter = attrgetter
        self.__attrgetter_search = attrgetter__search
        if forceverify:
            self.verify()
        self.endpoint = self.deflate_endpoint(self.endpoint)

    def verify(self):
        assert check_app(self.deflate_endpoint(self.endpoint))

    def deflate_endpoint(self, endpoint):
        if isinstance(endpoint, str):
            return getattr(self.__attrgetter, self.__attrgetter_search)(endpoint)
        return endpoint

            
class Map:
    def __init__(self, rules) -> None:
        self.rules = rules

    def find_rule(self, name):
        for r in self.rules:
            print(r.name)
            print(name)
            print(r.name==name)
            print(re.match(name, r.name))
            print([e.name for e in self.rules])

            if r.name == name or re.match((r.name), name):
                return r
            
        return Rule("err", Error("404 Not Found", f"{name} isn't a valid URL Route and wasn't found on the Server", fatal=False))