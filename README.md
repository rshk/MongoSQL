# MongoSQL

Because json-based queries are not for humans.


[![Build Status](https://travis-ci.org/rshk/MongoSQL.png)](https://travis-ci.org/rshk/MongoSQL)


## Package contents

* A ``parse(query)`` function that can be used to parse SQL queries
  and return objects that can then be used to perform actual queries.

  For complete SQL commands, a ``DatabaseOperation`` object will be returned.
  This object has an ``apply(db)`` name to apply the query on a database object
  (``MongoClient`` instance).

  For ``SELECT``s, a ``.query`` attribute is available, containing the query
  that would be executed on MongoDB (try
  ``parse('SELECT * FROM mytable WHERE one == "foo" and two == "bar"').query.to_mongo()``)

* A ``MongoSqlClient``, that can be used as a normal ``MongoClient`` (from which
  inherits), the only difference being returned databases has a ``.sql(query)`` method,
  allowing to run SQL queries directly.


## Usage

First, prepare a database with some data:

```python
from mongosql import MongoSqlClient

conn = MongoSqlClient('mongodb://localhost:27017')
db = conn.testdb

for item in 'World Spam Eggs Bacon Spam Spam Spam'.split():
	db.mycollection.save({'hello': 'Hello, {0}'.format(item)})
```

Then, we'll create a query:

```python
>>> list(db.sql('SELECT * FROM mycollection'))

[{u'_id': ObjectId('00112233445566778899AA00'), u'hello': u'Hello, World'},
{u'_id': ObjectId('00112233445566778899AA01'), u'hello': u'Hello, Spam'},
{u'_id': ObjectId('00112233445566778899AA02'), u'hello': u'Hello, Eggs'},
{u'_id': ObjectId('00112233445566778899AA03'), u'hello': u'Hello, Bacon'},
{u'_id': ObjectId('00112233445566778899AA04'), u'hello': u'Hello, Spam'},
{u'_id': ObjectId('00112233445566778899AA05'), u'hello': u'Hello, Spam'},
{u'_id': ObjectId('00112233445566778899AA06'), u'hello': u'Hello, Spam'}]
```

..yay! It worked!

Let's try with something more complex:

```python
>>> list(db.sql('SELECT * FROM mycollection WHERE hello == "Hello, World"'))

[{u'_id': ObjectId('00112233445566778899AA00'), u'hello': u'Hello, World'}]
```


## Example: search

```sql
SELECT field, field1, field2
FROM mycollection
WHERE field == 'value'
LIMIT 100 SKIP 20
SORT field1 ASC, field2 DESC
```

Becomes:

```python
db['mycollection'].find(
	{'field': 'value'},
	fields=['field', 'field1', 'field2'],
	limit=100,
	skip=20,
	sort={'field1': 1, 'field2': -1})
```


## Example: aggregation framework

(Only projections supported at the moment, more coming soon)

```sql
AGGREGATE article
PROJECT title = 1,
        stats = {
            pv = '$pageViews',
            foo = '$other.foo',
            dpv = '$pageViews' + 10,
        }
```

Becomes:

```python
db.article.aggregate([
    {'$project': {
        'title': 1,
        'stats': {
            'pv': "$pageViews",
            'foo': "$other.foo",
            'dpv': {'$add': ["$pageViews", 10]}
        },
    }}
])
```


## Reasons behind this

The reasons behind this project are:

* Many times I need to run test queries on a MongoDB server, eg. to see
  the status of the stored data, often with some aggregations / "GROUP BY".
  And I hate having to write JSON inline in the CLI, with all the
  (un)readability problems..

* In any case, I find that JSON queries tend to become unreadable quite soon,
  even in program code.

  And I hate writing things like: ``{'$and': [cond1, cond2, ...]}``.

  And I think that [polish notation] tends to become
  hard to follow quickly: compare, for example, ``(5 - 6) * 7``
  with ``* - 5 6 7`` (polish notation), ``(* (- 5 6) 7)`` (lisp)
  or, worse of them all, the mongodb way:
  ``{'$multiply': [{'$subtract': [5, 6]}, 7]}``...

[polish notation]: http://en.wikipedia.org/wiki/Polish_notation


## Reasons NOT behind this

The goal of this project is **not** to use MongoDB as a drop-in, web-scale
replacement for MySQL, to make your cats blog run the speed of light.
