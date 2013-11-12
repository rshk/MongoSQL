Base syntax
###########

The syntax of MongoSQL queries is similar to standard SQL, but uses some
MongoDB-specific additions / changes.

For example, names of keywords tend to follow names used in MongoDB
DSL instead of standard SQL (but, usually, SQL commands are supported as well).


Base types
==========

This is a description of the "base types" used by MongoSQL.
They are a mix between SQL and JSON objects.

Strings
-------

Strings can be single-quoted or double-quoted; they can contain C-style
escapes (``\a``, ``\b``, ``\f``, ``\n``, ``\r``, ``\t``, ``\v``) and
hexadecimal escapes (``\x##``).

Integers
--------

Integers follow the usual syntax ``[0-9]+``. Stuff like scientific notation,
hexadecimal numbers, etc. is not supported yet (but might be in the future).

Floats
------

Floating point numbers follow the ``[0-9]+\.[0-9]+`` syntax. Things like
``1.`` and ``.05`` are not supported since they can be misread and confusing.

Boolean
-------

Booleans are represented using the ``TRUE`` and ``FALSE`` keywords.

Null type
---------

The NULL type is just ``NULL``.

Symbol
------

The "symbol" (aka "ID") is just and identifier, which may be composed of
multiple dot-separated parts, matching ``[a-zA-Z_][a-zA-Z0-9_]*``.
The dollar ``$`` character might be added in future as well,
since it's used in MongoDB.

List
-----

Just a list of things. Delimited by brackets ``[`` and ``]``, items
are comma-separated. Supports trailing comma.

Map
-----

Maps are associations of ``(SYMBOL | STRING) : expression``.
They are delimited by braces (``{``, ``}``) and items can be specified
in two fashions:

* Assignment-like: ``{ one = 1, two = 2 }``
* JSON-like: ``{one: 1, two: 2}``

Trailing comma is suported as well.


Operators
=========

Operators and precedence rules come mostly from C and Python.

We prefer literal names for things like ``AND``, ``OR`` and ``NOT``,
for sake of clarity.


Arithmetic
----------

* ``+`` is the operator for sum
* ``-`` is the operator for subtraction
* ``*`` is the operator for multiplication
* ``/`` is the operator for division
* ``%`` is the operator for modulo
* We support unary ``-`` as well, for numbers (eg. ``-1``, ``-3.14``)


Comparison
----------

* ``==`` is the equality operator (eg. ``A == B``)
* ``!=`` is the inequality operator
* ``<``, ``<=``, ``>``, ``>=`` have the same meaning in C
* ``IN`` is the containment operator (eg. ``item IN list``)


Logical
-------

We use ``AND``, ``OR`` and ``NOT`` for their usual meaning.


Precedence
----------

See ``man operator``, it's copied from C.
You can override precedence using parenthesis (``(``, ``)``)
