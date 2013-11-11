from mongosql.lexer import lexer
from mongosql.parser import parser


def parse(query):
    return parser.parse(query, lexer=lexer)
