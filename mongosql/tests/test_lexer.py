from mongosql.lexer import lexer


def test_lexer_simple():
    lexer.input('SELECT one, two FROM table WHERE field = "value";')
    data = list(lexer)
    assert data[0].type == 'SELECT'
    assert data[1].value == 'one'
    pass
