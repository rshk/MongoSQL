from mongosql import parse
from mongosql.support import Comparison, SelectOperation


def test_simple_parsing():
    query = "SELECT * FROM mycollection WHERE field == 'value'"
    parsed = parse(query)
    assert isinstance(parsed, SelectOperation)
    assert parsed.collection == 'mycollection'
    assert parsed.fields is None
    assert isinstance(parsed.query, Comparison)
    assert parsed.query.to_mongo() == {'field': 'value'}

    class FakeCollection(object):
        def find(self, **kwargs):
            assert kwargs.keys() == ['spec']
            assert kwargs['spec'] == {'field': 'value'}

    parsed.apply({'mycollection': FakeCollection()})
    pass


def test_parsing_all_parts():
    query = """
    SELECT field, field1, field2
    FROM mycollection
    WHERE field == 'value'
    LIMIT 100 SKIP 20
    SORT field1 ASC, field2 DESC
    """
    parsed = parse(query)

    assert isinstance(parsed, SelectOperation)

    assert parsed.collection == 'mycollection'
    assert parsed.fields == ['field', 'field1', 'field2']

    assert isinstance(parsed.query, Comparison)
    assert parsed.query.to_mongo() == {'field': 'value'}

    assert parsed.limit == 100
    assert parsed.skip == 20
    assert parsed.sort == {'field1': 1, 'field2': -1}

    class FakeCollection(object):
        def find(self, **kwargs):
            assert set(kwargs.keys()) == set((
                'spec', 'fields', 'limit', 'skip', 'sort'))
            assert kwargs['spec'] == {'field': 'value'}
            assert kwargs['fields'] == ['field', 'field1', 'field2']
            assert kwargs['limit'] == 100
            assert kwargs['skip'] == 20
            assert kwargs['sort'] == {'field1': 1, 'field2': -1}

    parsed.apply({'mycollection': FakeCollection()})


def test_parsing_expressions():
    res = parse('SELECT * FROM coll WHERE foo == "Spam" AND bar == "Eggs"')
    # assert res.query.to_mongo() == {
    #     'foo': 'Spam',
    #     'bar': 'Eggs',
    # }
    assert res.query.to_mongo() == {
        '$and': [
            {'foo': 'Spam'},
            {'bar': 'Eggs'},
        ],
    }
    pass
