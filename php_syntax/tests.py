import unittest
import os
from php_syntax import load, loads, dumps

class TestPHPSyntax(unittest.TestCase):
    def  _basic(self, test):
        self.failUnlessEqual(test['string_scalar'], "forty two")
        self.failUnlessEqual(test['int_scalar'], 42)
        array = test['list_var']
        self.failUnlessEqual(array[0], 42);
        self.failUnlessEqual(array[1], "forty two");
        d = dict(test['dict_var']) # really -- sequence of tuples
        self.failUnlessEqual(d['string'], "forty two")
        self.failUnlessEqual(d['int'], 42)

    def test_basic(self):
        testfile = os.path.join(os.path.dirname(__file__), 
            'testdata', 'basic.php')
        test = load(testfile)
        self._basic(test)

    def test_basic_serialize_and_parse_again(self):
        testfile = os.path.join(os.path.dirname(__file__), 
            'testdata', 'basic.php')
        test = load(testfile)
        teststr = dumps(test)
        test2 = loads(teststr)
        self._basic(test2)


def test_suite():
    return unittest.makeSuite(TestPHPSyntax)
