"""PHP sucks, PHP grammar sucks twice.
   Python and pyparsing rules of course ;)

 simple PHP parser capable to read language resource files from mediawiki
 support only operator = and array() constructs
"""

from pyparsing import *

TRUE = Keyword("true").setParseAction( replaceWith(True) )
FALSE = Keyword("false").setParseAction( replaceWith(False) )
NULL = Keyword("null").setParseAction( replaceWith(None) )

def convertNumbers(s,l,toks):
    n = toks[0]
    try:
        return int(n)
    except ValueError, ve:
        return float(n)

def passthru(s, l, toks):
    return toks[0]

def make_tuple(toks):
    return tuple(*toks.asList())

php_singleQuote = Literal("'").setName("singleQuote")
php_doubleQuote = Literal('"').setName("doubleQuote")

php_ascii_octal = Suppress('0') + OneOrMore(Word(hexnums))\
                .setParseAction(lambda t: chr(int("".join(t),8)))
php_ascii_hex = Suppress("x") + OneOrMore(Word(hexnums))\
                .setParseAction(lambda t: chr(int("".join(t),16)))


php_escape_seq = Literal("\"").setParseAction( replaceWith("\"")) | \
    Literal("'").setParseAction( replaceWith("'")) | \
    Literal("n").setParseAction( replaceWith("\n")) | \
    Literal("r").setParseAction( replaceWith("\r")) | \
    Literal("t").setParseAction( replaceWith("\t")) | \
    Literal("\\").setParseAction( replaceWith("\\")) | \
    Literal("$").setParseAction( replaceWith("$")) | \
    Literal("{").setParseAction( replaceWith("{")) | \
    Literal("}").setParseAction( replaceWith("}")) | \
    Literal("[").setParseAction( replaceWith("]")) | \
    Literal("]").setParseAction( replaceWith("]")) | \
    php_ascii_octal | php_ascii_hex
php_escaped = Combine(Suppress('\\') + php_escape_seq)# .setDebug(flag=True)

# standard doubleQuotedString breaks on nested escaped and unescaped quotes
phpDoubleQuotedString = Combine(
     Suppress(php_doubleQuote)
    +ZeroOrMore(CharsNotIn('"\\') \
    |  php_escaped)
    +Suppress(php_doubleQuote))

# standard singleQuotedString breaks on nested escaped and unescaped quotes
phpSingleQuotedString = Combine(
    Suppress(php_singleQuote)
    +ZeroOrMore(CharsNotIn("'\\") | php_escaped)
    +Suppress(php_singleQuote))

phpString = ( phpSingleQuotedString | phpDoubleQuotedString  )

phpNumber = Combine( Optional('-') + ( '0' | Word('123456789',nums) ) +
                    Optional( '.' + Word(nums) ) +
                    Optional( Word('eE',exact=1) + Word(nums+'+-',nums) ) )

phpAtom =  ( phpString | phpNumber | TRUE | FALSE | NULL )
phpValue = Forward()
phpIdent = Word( alphas, alphanums+'_')
phpKey = phpIdent | phpString
phpPairs = Group(phpKey + Suppress("=>") + ( phpValue | phpKey ))
phpPairs.setParseAction(make_tuple)
phpMember = (phpPairs | phpAtom) # + Optional(Suppress(','))
phpMembers = ZeroOrMore(phpMember+Optional(Suppress(',')))
phpArray = Group(Suppress(Keyword('array')) + Suppress('(') + phpMembers + Suppress(')') ).setParseAction(lambda t: t.asList())
phpValue << ( phpAtom | phpArray )

phpExpr = Group(Suppress('$') + phpIdent + Suppress('=') + phpValue)
phpExpressions = ZeroOrMore(phpExpr+Suppress(';'))
phpFile = Group( Suppress('<?php') + phpExpressions + Optional(Suppress(Keyword('?>'))))
phpFile.ignore( cStyleComment )
phpFile.ignore( pythonStyleComment )


phpNumber.setParseAction( convertNumbers )
phpFile.setParseAction( passthru )
phpFile.enablePackrat()
#phpArray.setDebug(True)

if __name__ == "__main__":
    import sys
    import pprint
    results = phpFile.parseFile(sys.argv[1], parseAll=True)
    pprint.pprint( dict(results.asList()) )

