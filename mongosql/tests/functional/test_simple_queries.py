"""
MongoSQL - test simple queries
"""

import os
import pytest
import uuid

from mongosql import parse


MONGODB_URI = os.environ.get('MONGODB_URI')
MONGODB_NAME = os.environ.get('MONGODB_NAME') \
    or 'test_mongosql_{0}'.format(uuid.uuid4())


## Skip this module..
needs_mongo = pytest.mark.skipif('MONGODB_URI is None',
                                 reason='Requires MongoDB')


@pytest.fixture
def mongodb(request):
    import pymongo
    mongodb = pymongo.MongoClient(MONGODB_URI)

    def cleanup():
        mongodb.drop_database(MONGODB_NAME)

    request.addfinalizer(cleanup)
    return mongodb[MONGODB_NAME]


@needs_mongo
def test_simple_match(mongodb):
    objects = [
        {'item': 'apple', 'price': 10},
        {'item': 'banana', 'price': 5},
        {'item': 'pear', 'price': 12},
        {'item': 'pineapple', 'price': 50},
        {'item': 'grapes', 'price': 20},
    ]
    for item in objects:
        mongodb.mycollection.save(item)
    q = parse('SELECT * FROM mycollection')
    result = q.apply(mongodb)
    data = list(result)

    ## Objects got modified, they now have an _id
    ## and thus should match exactly the returned data!
    assert data == objects

    ## Now with a "WHERE" clause
    q = parse('SELECT * FROM mycollection WHERE item == "apple"')
    result = q.apply(mongodb)
    data = list(result)
    assert data == [objects[0]]

    ## Now with a "WHERE" clause
    q = parse("""
    SELECT * FROM mycollection
    WHERE item == "apple" OR item == "banana"
    """)
    result = q.apply(mongodb)
    data = list(result)
    assert data == [objects[0], objects[1]]

    ## Let's try the IN operator
    q = parse("""
    SELECT * FROM mycollection
    WHERE item IN ["apple", "banana"]
    """)
    assert q.query.to_mongo() == {'item': {'$in': ['apple', 'banana']}}
    result = q.apply(mongodb)
    data = list(result)
    assert data == [objects[0], objects[1]]

    ## Let's try the GT operator
    q = parse("SELECT * FROM mycollection WHERE price > 12")
    assert q.query.to_mongo() == {'price': {'$gt': 12}}
    result = q.apply(mongodb)
    data = list(result)
    assert data == [objects[3], objects[4]]

    ## Let's try the GTE operator
    q = parse("SELECT * FROM mycollection WHERE price >= 12")
    assert q.query.to_mongo() == {'price': {'$gte': 12}}
    result = q.apply(mongodb)
    data = list(result)
    assert data == [objects[2], objects[3], objects[4]]

    ## Let's try the LT operator
    q = parse("SELECT * FROM mycollection WHERE price < 12")
    assert q.query.to_mongo() == {'price': {'$lt': 12}}
    result = q.apply(mongodb)
    data = list(result)
    assert data == [objects[0], objects[1]]

    ## Let's try the LTE operator
    q = parse("SELECT * FROM mycollection WHERE price <= 12")
    assert q.query.to_mongo() == {'price': {'$lte': 12}}
    result = q.apply(mongodb)
    data = list(result)
    assert data == [objects[0], objects[1], objects[2]]

    ## Let's try with an OR
    q = parse("SELECT * FROM mycollection WHERE price <= 10 or price > 18")
    assert q.query.to_mongo() == {'$or': [
        {'price': {'$lte': 10}},
        {'price': {'$gt': 18}},
    ]}
    result = q.apply(mongodb)
    data = list(result)
    assert data == [objects[0], objects[1], objects[3], objects[4]]
