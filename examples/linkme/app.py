from elixir.application import Request, wrap_response, Headers
from sqlite3 import connect

class LinkMe:
    def __init__(self):
        self.db = connect("linkme.db")
        self.db.execute("CREATE TABLE IF NOT EXISTS links(shortlink TEXT, origin TEXT)")
        self.db.commit()

    def send(self, request):

        if request.path == "/": 
            return open("index.html").read()
        else:
            if request.path == "/link/new":
                return self.add_to_db(request.args.get("longurl"))
            else:
                cur = self.db.cursor()
                cur.execute("SELECT * FROM links WHERE shortlink LIKE ?", (request.path[1:],))
                return "R:"+cur.fetchone()[1]
            
    def add_to_db(self, link):
        import random, string
        shortlink = "".join(random.choices(string.ascii_letters, k=random.randint(8,16)))
        cur = self.db.cursor()
        cur.execute("INSERT INTO links VALUES(?,?)", (shortlink, link))
        self.db.commit()
        return f"Your Shortened Link is {shortlink}"
        
    def elix(self, environ, start_response):
        request = Request(environ)
        response_text = self.send(request)
        if response_text.startswith("R:"):
            from elixir.util import redirect
            return redirect(response_text[2:], start_response)
        
        resp =  wrap_response(response_text, start_response)
        return resp
    
    def __call__(self, environ, start_response):
        return self.elix(environ, start_response)
    
    
if __name__ == "__main__":
    from elixir.serving import run_server
    run_server(LinkMe())
