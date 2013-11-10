# MongoSQL

Because json-based queries are not for humans.


## Usage

First, prepare a database with some data:

```python
import pymongo
conn = pymongo.MongoClient('mongodb://localhost:27017')
db = conn.testdb

db.mycollection.save({'hello': 'Hello, World'})
db.mycollection.save({'hello': 'Hello, Spam'})
db.mycollection.save({'hello': 'Hello, Eggs'})
db.mycollection.save({'hello': 'Hello, Bacon'})
db.mycollection.save({'hello': 'Hello, Spam'})
db.mycollection.save({'hello': 'Hello, Spam'})
db.mycollection.save({'hello': 'Hello, Spam'})
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
{u'_id': ObjectId('527fe4a55bec3c3a494f8a84'), u'hello': u'Hello, World'}
{u'_id': ObjectId('527fe4ac5bec3c3a494f8a85'), u'hello': u'Hello, Spam'}
{u'_id': ObjectId('527fe4af5bec3c3a494f8a86'), u'hello': u'Hello, Eggs'}
{u'_id': ObjectId('527fe4b25bec3c3a494f8a87'), u'hello': u'Hello, Bacon'}
{u'_id': ObjectId('527fe4b45bec3c3a494f8a88'), u'hello': u'Hello, Spam'}
{u'_id': ObjectId('527fe4b55bec3c3a494f8a89'), u'hello': u'Hello, Spam'}
{u'_id': ObjectId('527fe4b55bec3c3a494f8a8a'), u'hello': u'Hello, Spam'}
```

...yay!

Let's try with something more complex:

```python
q = parse('SELECT * FROM mycollection WHERE hello == "Hello, World"')
data = q.apply(db)

for item in data:
	print item
```
```
{u'_id': ObjectId('527fe4a55bec3c3a494f8a84'), u'hello': u'Hello, World'}
```


## Examples

```sql
SELECT field, field1, field2
FROM mycollection
WHERE field == 'value'
LIMIT 100 SKIP 20
SORT field1 ASC, field2 DESC
```

More coming soon..

**Note:** The SQL we're using here is somehow specific to MongoDB.
For example, uses ``SORT`` instead of ``ORDER BY``, and the equality
comparison operator is ``==`` instead of ``=``.
