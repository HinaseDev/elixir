from typing import Union, List, Iterable

class ImmutableDict(dict):
    def __hash__(self):
        return id(self)

    def _immutable(self, *args, **kws):
        raise TypeError('object is immutable')

    __setitem__ = _immutable
    __delitem__ = _immutable
    clear       = _immutable
    update      = _immutable
    setdefault  = _immutable
    pop         = _immutable
    popitem     = _immutable

class Headers:
    def __init__(self, initial_headers: Union[dict, List[Iterable]]) -> None:
        self.__headers = []
        if isinstance(initial_headers, dict):
            for key, val in initial_headers.items():
                self.__headers.append((key, val))
        else:
            self.__headers = initial_headers

    def __getitem__(self, key):
        return self.get(key)
    
    def __setitem__(self, key, val):
        return self.add(key, val)
    
    
    
    def add(self, key, val):
        for i in self.as_wsgi:
            if key == i[0]:
                self.__headers[self.__headers.index(i)] = (key, val)
        self.__headers.append((key, val))
        return self

    def extend(self, headers: Union["Headers", dict, Iterable[Iterable]]):
        if isinstance(headers, "Headers"):
            self.extend(headers.as_wsgi)
        elif isinstance(headers, dict):
            for k, v in headers.items():
                self.add(k, v)

        else:
            for item in headers:
                self.add(*item)
        return self

    def get(self, key, default=None):
        for item in self.as_wsgi:
            if item[0] == key:
                return HeaderSet(item)
            
        return default

    @property
    def as_wsgi(self):
        return self.__headers

    
class HeaderSet:
    def __init__(self, *items) -> None:
        for item in items:
            key = item[0]
            val = item[1]
            setattr(self, f"__{key}", val)
            setattr(self, key, property(lambda: val))
        self.__setattr__ = self._immutable
        
    
    
    def _immutable(self, *args, **kws):
        raise TypeError('object is immutable')
    
    
    __setitem__ = _immutable
    __delitem__ = _immutable
    clear       = _immutable
    update      = _immutable
    setdefault  = _immutable
    pop         = _immutable
    popitem     = _immutable

InitialHeaders = Headers([("Server", "Elixir WSGI")])
InitialHeaders.add("Content-Type", "text/html")

