AGGREGATE queries
#################

The ``AGGREGATE`` query is used for performing ``aggregate()`` operations,
via the `aggregation framework`_.

.. _aggregation framework: http://docs.mongodb.org/manual/aggregation/


The base syntax is:  ``AGGREGATE <collection>``. The remaining part will be used
to build the aggregation pipeline.

.. warning::

    This part is still very work-in-progress and things described
    below may not corespond to the actual state of the project.

    Anyways, tests are being written in order to make things work
    this way.


The ``PROJECT`` command
=======================

Syntax: ``PROJECT <assignment-list>``

The ``PROJECT`` command allows an "assignment list", eg. a comma-separated list
of ``SYMBOL = expression`` items, that will be used to build the map in the ``$project``
command.

Example:

.. code-block:: sql

    AGGREGATE article
    PROJECT title = 1,
            stats = {
                pv = '$pageViews',
                foo = '$other.foo',
                dpv = '$pageViews' + 10,
            }

results in:

.. code-block:: python

    db.article.aggregate({'$project': {
        'title': 1,
        'stats': {
            'pv': "$pageViews",
            'foo': "$other.foo",
            'dpv': {'$add': ["$pageViews", 10]}
        },
    }})



The ``MATCH`` command
=====================

Syntax: ``MATCH <assignment-list>``

Results in: ``{'$match': ...}``


The ``LIMIT`` command
=====================

Syntax: ``LIMIT <num:int>``

Results in: ``{'$skip': num}``


The ``SKIP`` command
====================

Syntax: ``SKIP <num:int>``

Results in: ``{'$skip': num}``


The ``UNWIND`` command
======================

Syntax: ``UNWIND <name:symbol|string>``

Results in: ``{'$unwind': name}``


The ``GROUP`` command
=====================

Syntax: ``GROUP [ BY <expression> , ] <assignment-list>``

Results in: ``{'$group': assignment_list}``.

If the ``BY <expression>`` part is present, a key named ``_id``
will be added to the assignment list before using as argument
to ``$group``.


The ``SORT`` command
====================

Syntax: ``SELECT <sort-spec>``

Results in: ``{'$sort': sort_spec}``.

Same as in the ``SELECT`` query: a list of ``<field> <direction>``
items will be converted in a list of ``(field, direction)`` tuples.

Supported directions are ``ASC`` and ``DESC``.


The ``GEO_NEAR`` command
========================

.. todo:: write this
