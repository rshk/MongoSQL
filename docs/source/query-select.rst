SELECT queries
##############

SELECT queries are converted in ``.find()`` operations.

The base syntax is ``SELECT <fields> FROM <collection>``, where ``fields``
is a comma-separated list of symbols, representing field names, or the literal
"``*``" meaning "all fields". ``collection`` is a symbol or string, representing
the collection name.

.. note::
    We currently don't support field aliasing (eg. ``SELECT field AS foo, field1 AS bar``,
    as MongoDB doesn't as well..)

Example:

.. code-block:: sql

    SELECT title, body FROM blog_posts

Will result in the call of:

.. code-block:: python

    db.blog_posts.find(fields=['title', 'body'])


The ``WHERE`` clause
====================

The ``WHERE <expression>`` clause can be used to specify a condition.

Example:

.. code-block:: sql

    SELECT * FROM blog_posts WHERE author = "Mr.X" and reads > 100

results in:

.. code-block:: python

    db.blog_posts.find({
        '$and': [
            {'author': 'Mr.X'},
            {'reads': {'$gt': 100}}
        ]
    })

(yes, of course this can be made greatly more intelligent, for example that
"and" can be converted in ``{'author': 'Mr.X', 'reads': {'$gt': 100}}``,
but that's not always trivial and requires some thinking about..)


``LIMIT`` and ``SKIP``
======================

To retrieve only a "window" of results, use the ``LIMIT <int>`` and ``SKIP <int>``
clauses.

Example:

.. code-block:: sql

    SELECT * FROM blog_posts LIMIT 10 SKIP 20

results in:

.. code-block:: python

    db.blog_posts.find(limit=10, skip=20)


Ordering
========

To order, you can use one of the following (equivalent) keywords:
``SORT``, ``SORT BY``, ``ORDER``, ``ORDER BY``.

Example:

.. code-block:: sql

    SELECT * FROM blog_posts ORDER BY author ASC, date DESC

results in:

.. code-block:: python

    db.blog_posts.find(sort=[('author', 1), ('date', -1)])
