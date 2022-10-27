import site
from elixir.middleware import ImmutableDict, Headers
import cgi

class Request:
    def __init__(self, environ) -> None:
        self.environ = environ
        self.method = environ["REQUEST_METHOD"]
        self.path = environ["PATH_INFO"]
        self.args = self.parseqs(environ["QUERY_STRING"])
        self.port = environ["SERVER_PORT"]
        self.host = environ["SERVER_NAME"]
        self.protocol_version = environ["SERVER_PROTOCOL"]
        self.url = f"{self.parseproto()}://{self.host}:{self.port}{self.path}"
        self.headers = Headers([])
        if self.method == "POST":
            self.post = cgi.FieldStorage(fp=environ['wsgi.input'],environ=environ, keep_blank_values=1)
        for k in environ.keys():
            if k.startswith("HTTP_"):
                self.headers.add(k[5:], environ[k])

    def parseproto(self):
        return self.protocol_version.split("/")[0].lower()
            
    def parseqs(self, string):
        """
        Parse a Query String into a Dictionary
        >>> parseqs("s=HelloWorld&Foo=Bar")
        ImmutableDict({"s":"HelloWorld","Foo":"Bar"})
        """
        if not string: return ImmutableDict()
        dct = {}
        for s in string.split("&"):
            key, val = s.split("=")
            dct[key] = val
        
        return ImmutableDict(**dct)
    