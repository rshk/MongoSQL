from mongosql.lexer import lexer


def _check_parsed(data, expected):
    assert len(data) == len(expected)
    for i, (typ, val) in enumerate(expected):
        assert data[i].type == typ
        assert data[i].value == val


def test_lexer_simple():
    lexer.input("""
    SELECT one, two FROM table
    MATCH field == "value"
    GROUP _id = name, count = sum(1);
    """)
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
    _check_parsed(list(lexer), expected)


def test_lexer_comments():
    lexer.input("""
    SELECT one, two  # This is a comment
    FROM table  // The table!
    SORT one ASC;
    -- Will ignore this too!
    """)
    expected = [
        ('SELECT', 'SELECT'),
        ('SYMBOL', 'one'),
        ('COMMA', ','),
        ('SYMBOL', 'two'),
        ('FROM', 'FROM'),
        ('SYMBOL', 'table'),
        ('SORT', 'SORT'),
        ('SYMBOL', 'one'),
        ('ASC', 'ASC'),
        ('SEMICOLON', ';'),
    ]
    _check_parsed(list(lexer), expected)


def test_lexer_comments_multiline():
    lexer.input("""
    SELECT one, /* two, */ three
    FROM table /*
    This just a comment
    */ SORT one ASC;
    """)
    expected = [
        ('SELECT', 'SELECT'),
        ('SYMBOL', 'one'),
        ('COMMA', ','),
        ('SYMBOL', 'three'),
        ('FROM', 'FROM'),
        ('SYMBOL', 'table'),
        ('SORT', 'SORT'),
        ('SYMBOL', 'one'),
        ('ASC', 'ASC'),
        ('SEMICOLON', ';'),
    ]
    _check_parsed(list(lexer), expected)

    lexer.input("""
    SELECT one, /* two, */ three /* , four */
    FROM table /*
    This just a comment: /* <-- This is cool
    */ SORT one ASC;
    """)
    expected = [
        ('SELECT', 'SELECT'),
        ('SYMBOL', 'one'),
        ('COMMA', ','),
        ('SYMBOL', 'three'),
        ('FROM', 'FROM'),
        ('SYMBOL', 'table'),
        ('SORT', 'SORT'),
        ('SYMBOL', 'one'),
        ('ASC', 'ASC'),
        ('SEMICOLON', ';'),
    ]
    _check_parsed(list(lexer), expected)

    lexer.input("""
    Nesting /* comments is /* not */ allowed: */ is starslash;
    """)
    expected = [
        ('SYMBOL', 'Nesting'),
        ('SYMBOL', 'allowed'),
        ('COLON', ':'),
        ('STAR', '*'),
        ('SLASH', '/'),
        ('SYMBOL', 'is'),
        ('SYMBOL', 'starslash'),
        ('SEMICOLON', ';'),
    ]
    _check_parsed(list(lexer), expected)
