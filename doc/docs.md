# Elixir
Welcome to the Documentation for the ELIXIR Package. In the following Pages, we'll learn how to make a simple TinyURL Clone.  
If you came here to read the *actual* Documentation, click [here](#Reference) instead.

## 0. - A Quick Overview of WSGI 
I'll go with assuming that you'e already installed Elixir. That's great!  
Now, I stated Elixir was a WSGI Wrapper. However, People might be unfamiliar  
with the Concept of WSGI: WSGI is short for "Web Server Gateway Interface" and is  
a convention that ensures your App can speak with your Server and - more importantly -  
that your Web Apps can work nicely together.


This is how a simple Hello-World-App in WSGI would look like without the help of Elixir
```py
def app(environ, start_response):
    start_response("200, OK", [("Content-Type", "text/plain")])
    return ["Hello World".encode("utf8")]
```

This is how WSGI works. It passes an "environ" dict and a `start_response` Callable.  
The environ-dict contains every Information your App requires to run, whereas `start_response`  
tells WSGI how your Server reacted to the request.

Although this looks simple, it is kind of hard and/or annoying to call the start_response() every time,  
let alone turn the response content into an encoded list every time you want to return it.
Let's use Elixir to make this look a bit nicer:  

```py
from elixir.application import wrap_response

def app(environ, start_response):
    return wrap_response("Hello World", start_response, mimetype="text/plain")
```

And, just to show how simple working with Elixir is, let's expand this script,  
so it uses the Query String. "Query String" is everything after the `?` in your URL Bar.

```py
from elixir.application import wrap_response, Request

def app(environ, start_response):
    request = Request(environ)
    text = f"Hello, {request.args.get('name', 'World')}"
    return wrap_response(text, start_response, mimetype="text/plain")
```

If we now were to pass `?name=Hinase`, the response text would be `Hello, Hinase`, and that's how WSGI works.+


## 1. A Basic Structure
Now, after this short Intro, let's actually get started on our Link Shortener! I've decided to call it "LinkMe", but that's up to you.  

We're gonna need some Imports first
```py
from elixir.application import Request, wrap_response, Headers
from sqlite3 import connect
```

Next, let's define our Main Class:
```py
class LinkMe:
    def __init__(self):
        self.db = connect("linkme.db")

    def send(self, request):
        return "Hello World"
    
    def elix(self, environ, start_response):
        request = Request(environ)
        response_text = self.send(request)
        resp =  wrap_response(response_text, start_response)
        return resp
    
    def __call__(self, environ, start_response):
        return self.elix(environ, start_response)
```

And lastly a few lines to run the app
```py
if __name__ == "__main__":
    from elixir.serving import run_server
    run_server(LinkMe())
```

And now, if we visit http://localhost:1234, we'll read "Hello World"!

### 1.5. - The Database
Whoops, looks like we forgot to initialize the Database!  
Since this script uses SQLite3 for Database Work, let's add
this to our `__init__`:
```py
self.db.execute("CREATE TABLE IF NOT EXISTS links(shortlink TEXT, origin TEXT)")
self.db.commit()
```

## 2. - The Routing
Alright, so far we've made a *lot* of single-Paged Apps. However a Link shortener usually isn't limited to just one Page.  
Luckily, we got the `Request` object.

So, in our send-function, let's cut out the old code and paste this in, so it looks like this:

```py

def send(self, request):
    if request.path == "/": 
        return "Hello World"
    else:
        return "404, not found"
```

Don't worry, we'll come back to this later.

## 3. - Adding new Links
Finally, some actual functionality!

Lets first create a file called `index.html`, with this content:

```html
<h1>LinkMe URL Shortener</h1>
<div style="border: 1px solid #000; border-radius: 25px">
    <form action="/link/new">
        <input name="longurl" placeholder="Paste your Long URL Here!" required>
        <input type="submit">
    </form>
</div>
```

and in our send Function:
```py
if request.path == "/": 
    return open("index.html").read()
else:
    if request.path == "/link/new":
        return self.add_to_db(request.args.get("longurl"))

```

With this, we're almost done with half of the work! We just need to insert this into our database, and voila, 50% of the work is done

## 4. - Shortening the Link

How do we actually shorten this link? We'll be using a combination of Python's Random and String Library to randomize the letters.

```py


def add_to_db(self, link):
    import random, string
    shortlink = "".join(random.choices(string.ascii_letters, k=random.randint(8,16)))
    cur = self.db.cursor()
    cur.execute("INSERT INTO links VALUES(?,?)", (shortlink, link))
    self.db.commit()
    return f"Your Shortened Link is {shortlink}"
```

This might look like a lot, but it's actually very simple: Let's go through this Line by Line.
First, we import the random and string library. These are built in, so there's no need to  
install anything. Then, we join a couple of randomly chosen letters from the string.ascii_letters Constant.  
Then we're writing these changes to the database and lastly return the new Link.

## 5. - The last pieces

So, our last step is, if someone calls /\<shortlink\>, get the Link out of the Database and redirect to it.
We do that by putting one last `else` after the second if from Step 3.
```py

else:
    cur = self.db.cursor()
    cur.execute("SELECT * FROM links WHERE shortlink LIKE ?", (request.path[1:], ))
    return "R:"+cur.fetchone()[1]
```

But wait, one last thing has to be done:

Inside our `def elix`, just after getting the response Text, we paste this:

```py

if response_text.startswith("R:"):
    from elixir.util import redirect
    return redirect(response_text[2:], start_response)
```
