from mongosql.parser import parser
from mongosql.lexer import lexer
from mongosql.support import Comparison


def test_simple_parsing():
    query = "SELECT * FROM mycollection WHERE field == 'value'"
    #query = "SELECT * FROM mycollection"
    parsed = parser.parse(query, lexer=lexer)
    assert parsed.collection == 'mycollection'
    assert parsed.fields is None
    assert isinstance(parsed.query, Comparison)
    assert parsed.query.to_mongo() == {'field': {'$eq': 'value'}}
    pass
