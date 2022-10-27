from elixir.application import WSGI, wrap_response

sessdict = {}

def Error(code, info, fatal=True):
    sessdict["error"] = [code, info]

    if fatal: raise Exception(f"{code}: {info}")
    else:
        return WSGI(error_page)
    
def abort(code, info="The Web App aborted your Request"):
    return Error(code, info, False)

def error_page(req,res):
    text = "".join(f"""
<h1>{sessdict['error'][0]}</h1>
<p>{sessdict['error'][1]}</p>
    """.splitlines())
    return wrap_response(text, res, status_code=str(sessdict["error"][0]))

