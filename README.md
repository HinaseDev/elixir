# Elixir
Elixir is a simplistic, fast Wrapper around Python's WSGIRef. It allows quick, simple creation of WSGI Apps and  
can even be used when building Frameworks.

Keep in mind, Elixir is *not* a Framework, it's a *wrapper* that can be used to build Frameworks.  


### Installation
Install using pip:
```
pip install -U git+https://github.com/hinasedev/elixir.git
```

### A Simple Example

```py
from elixir.application import WSGI, wrap_response

def app(request, response):
    return wrap_response("Hello World!", response)

if __name__ == "__main__":
    from elixir.serving import run_server
    run_server(WSGI(app), "localhost", 1234)
```
Now, just visit http://localhost:1234 in your browser and you should see a "HELLO WORLD"
