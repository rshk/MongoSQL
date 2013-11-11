"""
Tests for the MongoSQL client
"""

import pytest

from .test_simple_queries import MONGODB_URI, MONGODB_NAME, needs_mongo
from mongosql import MongoSqlClient


@pytest.fixture
def mongodb(request):
    mongodb = MongoSqlClient(MONGODB_URI)

    def cleanup():
        mongodb.drop_database(MONGODB_NAME)

    request.addfinalizer(cleanup)
    return mongodb[MONGODB_NAME]


@needs_mongo
def test_mongosql_client_simple_queries(mongodb):
    objects = [
        {'item': 'apple', 'price': 10},
        {'item': 'banana', 'price': 5},
        {'item': 'pear', 'price': 12},
        {'item': 'pineapple', 'price': 50},
        {'item': 'grapes', 'price': 20},
    ]
    for item in objects:
        mongodb.mycollection.save(item)
    result = mongodb.sql('SELECT * FROM mycollection')
    data = list(result)

    ## Objects got modified, they now have an _id
    ## and thus should match exactly the returned data!
    assert data == objects

    ## Now with a "WHERE" clause
    result = mongodb.sql('SELECT * FROM mycollection WHERE item == "apple"')
    data = list(result)
    assert data == [objects[0]]

    ## Let's try the IN operator
    result = mongodb.sql("""
    SELECT * FROM mycollection
    WHERE item IN ["apple", "banana"] OR price > 20
    """)
    data = list(result)
    assert data == [objects[0], objects[1], objects[3]]
