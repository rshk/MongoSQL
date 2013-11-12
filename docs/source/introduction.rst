Introduction
############

Reasons behind this
===================

The reasons behind this project are:

* Many times I need to run test queries on a MongoDB server, eg. to see
  the status of the stored data, often with some aggregations / "GROUP BY".
  And I hate having to write JSON inline in the CLI, with all the
  (un)readability problems..

* In any case, I find that JSON queries tend to become unreadable quite soon,
  even in program code.

  And I hate writing things like: ``{'$and': [cond1, cond2, ...]}``.

  And I think that `polish notation`_ tends to become
  hard to follow quickly: compare, for example, ``(5 - 6) * 7``
  with ``* - 5 6 7`` (polish notation), ``(* (- 5 6) 7)`` (lisp)
  or, worse of them all, the mongodb way:
  ``{'$multiply': [{'$subtract': [5, 6]}, 7]}``...

.. _polish notation: http://en.wikipedia.org/wiki/Polish_notation


Reasons NOT behind this
=======================

The goal of this project is **not** to use MongoDB as a drop-in, web-scale
replacement for MySQL, to make your cats blog run the speed of light!


Example usage
=============

Everyone likes examples! All right then..

First, let's connect to our MongoDB server:

.. code-block:: python

    from mongosql import MongoSqlClient
    conn = MongoSqlClient('mongodb://localhost:27017')

Then, we'll populate the database a bit, using the
standard MongoDB way (``MongoSqlClient`` extends ``pymongo.MongoClient``):

.. code-block:: python

    db = conn.my_test_db
    for item in 'World Spam Eggs Bacon Spam Spam Spam'.split():
	db.mycollection.save({'hello': 'Hello, {name}!'.format(name=item)})

Ok, it's time for our first SQL-based query to MongoDB!

.. code-block:: python

    result = db.sql('SELECT * FROM mycollection WHERE hello == "Hello, Spam!"')

If you inspect the contents of result, you'll see it worked!

.. code-block:: python

    for item in result:
        print(item)

::

    {u'_id': ObjectId('....01'), u'hello': u'Hello, Spam'}
    {u'_id': ObjectId('....04'), u'hello': u'Hello, Spam'}
    {u'_id': ObjectId('....05'), u'hello': u'Hello, Spam'}
    {u'_id': ObjectId('....06'), u'hello': u'Hello, Spam'}

Now, experiment with more complex queries. Some examples:

* ``... WHERE field == "value" AND other == "value2"``
* ``... WHERE field in ['foo', 'bar']``
* ``... WHERE price < 10 OR price > 100``

(Quite likely, you'll experience issues at a certain point.
Please feel free to `report issues <https://github.com/rshk/MongoSQL/issues>`_
to help speeding up the development!)
