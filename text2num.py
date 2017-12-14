import re

Small = {
    'zero': 0,
    'un': 1,
    'deux': 2,
    'trois': 3,
    'quatre': 4,
    'cinq': 5,
    'six': 6,
    'sept': 7,
    'huit': 8,
    'neuf': 9,
    'dix': 10,
    
}

class NumberException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

def text2num(s):
    a = re.split(r"[\s-]+", s)
    g = 0
    for w in a:
        x = Small.get(w, None)
        if x is not None:
            g += x
        else:
            raise NumberException("Unknown number: "+w)
    return g
    
