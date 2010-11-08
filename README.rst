php_syntax parser for python
============================

This is simple and small library  written for various data structures contained
in php sources. Originnaly developed for reading MediaWiki LanguageXX.php,
library was extended by simple serializer, and API was changed in same manner
as in pickle and json serializers.

API
---
Library provides ``load`` and ``loads`` to load php data structures from
file or string.  Structure always loaded as dict with defined variables as
keys.

Use ``dump`` / ``dumps`` to save data back.


Supported constructions
-----------------------

We support following PHP operators:  ``=`` and ``array``.
Both scalars and key-value pairs supported in arrays.
Values can be integer, string or ``true``/``false``/``none``.

Floats are not supported at this moment.

