from mongosql.lexer import lexer


def test_lexer_simple():
    lexer.input("""
    SELECT one, two FROM table
    MATCH field == "value"
    GROUP _id = name, count = sum(1);
    """)
    data = list(lexer)
    expected = [
        ('SELECT', 'SELECT'),
        ('SYMBOL', 'one'),
        ('COMMA', ','),
        ('SYMBOL', 'two'),
        ('FROM', 'FROM'),
        ('SYMBOL', 'table'),
        ('MATCH', 'MATCH'),
        ('SYMBOL', 'field'),
        ('DBLEQUAL', '=='),
        ('STRING', '"value"'),

        ('GROUP', 'GROUP'),
        ('SYMBOL', '_id'),
        ('EQUAL', '='),
        ('SYMBOL', 'name'),
        ('COMMA', ','),
        ('SYMBOL', 'count'),
        ('EQUAL', '='),
        ('SYMBOL', 'sum'),
        ('LPAREN', '('),
        ('INTEGER', 1),
        ('RPAREN', ')'),
        ('SEMICOLON', ';'),
    ]
    assert len(data) == len(expected)
    for i, (typ, val) in enumerate(expected):
        assert data[i].type == typ
        assert data[i].value == val
