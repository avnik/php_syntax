"""
We provide pickle/json style API, because we read only data structures declared
in .php files.
"""
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from php_syntax.php import phpFile
from php_syntax.writer import dump

def load(filename):
    ast = phpFile.parseFile(filename, parseAll=True)
    return dict(ast.asList())

def loads(string):
    ast = phpFile.parseString(string, parseAll=True)
    return dict(ast.asList())

def dumps(obj):
    sio = StringIO()
    dump(obj, sio)
    return sio.getvalue()

__all__ = ["load", "loads", "dump", "dumps"]
