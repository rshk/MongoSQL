"""
Support objects for MongoSQL
"""


def to_mongo(obj):
    if hasattr(obj, 'to_mongo'):
        return obj.to_mongo()
    return obj


class DatabaseOperation(object):
    pass


class SelectOperation(DatabaseOperation):
    def __init__(self, collection, query=None, fields=None, limit=None,
                 skip=None, sort=None):
        self.collection = collection  # string
        self.query = query  # Query() object
        self.fields = fields  # list
        self.limit = limit  # int
        self.skip = skip  # int
        self.sort = sort  # {field: direction}

    def apply(self, db):
        kwargs = {}
        if self.query is not None:
            kwargs['spec'] = to_mongo(self.query)
        if self.fields is not None:
            assert isinstance(self.fields, (list, tuple))
            kwargs['fields'] = self.fields
        if self.limit is not None:
            assert isinstance(self.limit, (int, long))
            kwargs['limit'] = self.limit
        if self.skip is not None:
            assert isinstance(self.skip, (int, long))
            kwargs['skip'] = self.skip
        if self.sort is not None:
            kwargs['sort'] = to_mongo(self.sort)
        return db[self.collection].find(**kwargs)


class Symbol(object):
    """Used to represent generic symbols"""

    def __init__(self, name):
        self.name = name

    def to_mongo(self):
        return self.name  # used as-is..


class FunctionCall(object):
    def __init__(self, function, args):
        self.function = function
        self.args = args

    def to_mongo(self):
        return {
            '${0}'.format(self.function): [
                to_mongo(a) for a in self.args
            ]
        }


class NamedExpression(object):
    def __init__(self, name, expression):
        self.name = name
        assert isinstance(self.name, basestring)
        self.expression = expression

    def to_mongo(self):
        return {self.name: to_mongo(self.expression)}


class Expression(object):
    pass


class OperationBase(Expression):
    operator_names = {}

    def __init__(self, first, operator, second):
        self.first = first
        self.operator = operator.upper()  # Always uppercase..
        self.second = second

    def _get_operator(self):
        if self.operator in self.operator_names:
            return self.operator_names[self.operator]
        raise ValueError("Invalid operator: {0!r}".format(self.operator))

    def to_mongo(self):
        return {
            self._get_operator(): [
                to_mongo(x) for x in (self.first, self.second)]}


class Operation(OperationBase):
    operator_names = {
        '+': '$add',
        '-': '$subtract',
        '*': '$multiply',
        '/': '$divide',
        '%': '$mod',
    }


class Comparison(OperationBase):
    operator_names = {
        '<': '$lt',
        '<=': '$lte',
        '>': '$gt',
        '>=': '$gte',
        '==': '$eq',
        '!=': '$ne',
    }

    def to_mongo(self):
        # If the first one is a symbol, we're ok
        # Else, not sure on how to handle this..
        if isinstance(self.first, Symbol):
            op = self._get_operator()
            if op == '$eq':
                return {to_mongo(self.first): to_mongo(self.second)}
            return {to_mongo(self.first): {op: to_mongo(self.second)}}
        raise NotImplementedError("What should I do?")


class LogicalOperation(OperationBase):
    operator_names = {
        'AND': '$and',
        'OR': '$or',
    }


class LogicalNot(object):
    def __init__(self, expression):
        self.expression = expression

    def to_mongo(self):
        return {'$not': to_mongo(self.expression)}
