# MongoSQL

Because json-based queries are not for humans.


[![Build Status](https://travis-ci.org/rshk/MongoSQL.png)](https://travis-ci.org/rshk/MongoSQL)


## Usage

First, prepare a database with some data:

```python
import pymongo
conn = pymongo.MongoClient('mongodb://localhost:27017')
db = conn.testdb

for item in 'World Spam Eggs Bacon Spam Spam Spam'.split():
	db.mycollection.save({'hello': 'Hello, {0}'.format(item)})
```

Then, we'll create a query:

```python
from mongosql import parse

q = parse('SELECT * FROM mycollection')
data = q.apply(db)

for item in data:
	print item
```
```
{u'_id': ObjectId('00112233445566778899AA00'), u'hello': u'Hello, World'}
{u'_id': ObjectId('00112233445566778899AA01'), u'hello': u'Hello, Spam'}
{u'_id': ObjectId('00112233445566778899AA02'), u'hello': u'Hello, Eggs'}
{u'_id': ObjectId('00112233445566778899AA03'), u'hello': u'Hello, Bacon'}
{u'_id': ObjectId('00112233445566778899AA04'), u'hello': u'Hello, Spam'}
{u'_id': ObjectId('00112233445566778899AA05'), u'hello': u'Hello, Spam'}
{u'_id': ObjectId('00112233445566778899AA06'), u'hello': u'Hello, Spam'}
```

..yay!

Let's try with something more complex:

```python
>>> q = parse('SELECT * FROM mycollection WHERE hello == "Hello, World"')
>>> data = q.apply(db)

>>> for item in data:
...     print item

{u'_id': ObjectId('00112233445566778899AA00'), u'hello': u'Hello, World'}
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


## Example: projection framework

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
