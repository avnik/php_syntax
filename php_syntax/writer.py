"""
Serialize data structure back into .php syntax.
This code written for testing purposes
"""
def _serialize_string(fp, s):
    """Very quick and very dirty"""
    fp.write(repr(s)) 

def _serialize_value(fp, obj, strict=False):
    def _serialize_pair(key, val):
        _serialize_value(fp, key)
        fp.write(" => ")
        _serialize_value(fp, val)
        fp.write(', ')
    def _serialize_list(lst):
        fp.write("array( ");
        for each in lst:
            if isinstance(each, tuple) and len(each) == 2:
                (key, val) = each
                _serialize_pair(key, val)
            else:
                _serialize_value(fp, each, strict)
                fp.write(', ')
        fp.write(")");

    def _serialize_dict(dct):
        fp.write("array( ")
        for key, val in dct.iteritems():
            _serialize_pair(key, val)
        fp.write(")")
    if isinstance(obj, str):
        _serialize_string(fp, obj)
    elif isinstance(obj, unicode):
        _serialize_string(fp, obj.encode('utf-8'))
    elif isinstance(obj, list):
        _serialize_list(obj)
    elif isinstance(obj, dict):
        _serialize_dict(obj)
    elif isinstance(obj, (int, float, long)):
        fp.write(str(obj))
    elif obj is True:
        fp.write("true")
    elif obj is False:
        fp.write("false")
    elif obj is None:
        fp.write("none")
    else:
        if not strict and hasattr(obj, '__str__'):
            _serialize_string(fp, str(obj))
            return
        raise RuntimeError("Can't serialize '%s'" % repr(obj))

def dump(obj, fp, strict=True):
    fp.write("<?php\n");
    for var, value  in obj.iteritems():
        fp.write("$%s = " % var)
        _serialize_value(fp, value, strict)
        fp.write(";\n")
    fp.write("?>\n");
