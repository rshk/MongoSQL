"""
Lexer for MongoSQL expressions
"""

import re

import ply.lex as lex


tokens = [
    'COMMENT',  # Comments --.*

    ## Parenthesis, braces and brackets
    'LBRACE',
    'RBRACE',
    'LBRACKET',
    'RBRACKET',
    'LPAREN',
    'RPAREN',

    ## Fixed symbols
    'EQUAL',
    'COLON',
    'COMMA',
    'STAR',

    ## Base types
    'STRING',
    'INTEGER',
    'FLOAT',
    'TRUE',
    'FALSE',
    'NULL',
    'SYMBOL',
]

## Order matters!
token_symbols = [
    ('LBRACE', '{'),
    ('RBRACE', '}'),
    ('LBRACKET', '['),
    ('RBRACKET', ']'),
    ('LPAREN', '('),
    ('RPAREN', ')'),

    #('COLON', ':'),  # for stuff -> which stuff??
    ('SEMICOLON', ';'),  # terminator
    ('COMMA', ','),  # separator
    ('DBLEQUAL', '=='),  # equality
    ('EQUAL', '='),  # assignment
    ('GT', '>'),  # comparison
    ('GTE', '>='),  # comparison
    ('LT', '<'),  # comparison
    ('LTE', '<='),  # comparison
    ('MINUS', '-'),  # operator
    ('NE', '!='),  # comparison
    ('PERCENT', '%'),  # operator
    ('PLUS', '+'),  # operator
    ('SLASH', '/'),  # operator
    ('STAR', '*'),  # operator
]


globs = globals()
for tk, tkval in token_symbols:
    tokens.append(tk)
    globs['t_' + tk] = re.escape(tkval)


reserved = [
    ## Used for "normal" queries -> applied on a connection
    'SELECT',
    'FROM',

    ## For naming stuff
    'AS',

    ## Logical
    'AND',
    'OR',
    'NOT',

    ## Sorting constants
    'ASC',
    'DESC',

    ## We use mongodb terminology here!
    'PROJECT',
    'MATCH',
    'LIMIT',
    'SKIP',
    'UNWIND',
    'GROUP',
    'SORT',
    'GEO_NEAR',
]

tokens += reserved

## Whitespace gets ignored
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    raise TypeError("Unknown text {0!r}".format(t.value,))


def t_COMMENT(t):
    r'(--|\#|//).*'  # We accept sql-style, python-style an c++-style comments
    # todo: how to support c-style multiline /* comments */ ?
    return None  # Just skip this token

##------------------------------------------------------------
## Simple tokens
##------------------------------------------------------------

# t_LBRACE = r'\{'
# t_RBRACE = r'\}'
# t_LBRACKET = r'\['
# t_RBRACKET = r'\]'
# t_LPAREN = r'\('
# t_RPAREN = r'\)'
# t_EQUAL = r'='
# t_COLON = r':'
# t_COMMA = r','
# t_STAR = r'\*'

# Symbols can have dots
symbol_part = r'([a-zA-Z_][a-zA-Z0-9_]*)'


@lex.TOKEN(r'{sp}(\.{sp})*'.format(sp=symbol_part))
def t_SYMBOL(t):
    t_name = t.value.upper()
    t.type = t_name if (t_name in reserved) else 'SYMBOL'
    return t

##------------------------------------------------------------
## String tokenization
## We accept both single-quoted and double-quoted strings
## Strings are in form: <flags>"<content>" (or single quotes)
##------------------------------------------------------------

simple_escape = r"""([a-zA-Z._~!=&\^\-\\?'"])"""
decimal_escape = r"""(\d+)"""
hex_escape = r"(x[0-9a-fA-F]+)"
escape_sequence = ''.join((
    r'(\\(', simple_escape, '|', decimal_escape, '|', hex_escape, '))'))

# Double-quoted string
string_double_char = ''.join((r'([^"\\\n]|', escape_sequence, ')'))
string_double = ''.join(('"', string_double_char, '*"'))

# Single-quoted string
string_single_char = ''.join((r"([^'\\\n]|", escape_sequence, ")"))
string_single = ''.join(("'", string_single_char, "*'"))


@lex.TOKEN('|'.join((string_single, string_double)))
def t_STRING(t):
    assert t.value[0] == t.value[-1]
    assert t.value[0] in ('"', "'")
    # todo: already return the string with escapes processed?
    return t


##------------------------------------------------------------
## Numbers tokenization
##------------------------------------------------------------

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t


##------------------------------------------------------------
## Boolean/None
##------------------------------------------------------------

def t_TRUE(t):
    r'true'
    t.value = True
    return t


def t_FALSE(t):
    r'false'
    t.value = False
    return t


def t_NULL(t):
    r'null'
    t.value = None
    return t


lexer = lex.lex()