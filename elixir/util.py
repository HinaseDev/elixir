from elixir.middleware import Headers, InitialHeaders

def redirect(to, start_response, *, headers: Headers=InitialHeaders, status_code="308 Redirect", after=0):
    """
    Redirects automatically
    """
    headers["refresh"] = f'{after};url={to}'


    start_response(status_code, headers.as_wsgi)
    return ["".encode("utf8")]
