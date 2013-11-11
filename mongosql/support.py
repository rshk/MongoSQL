"""
Support objects for MongoSQL
"""

import copy


def to_mongo(obj):
    if hasattr(obj, 'to_mongo'):
        return obj.to_mongo()
    return copy.deepcopy(obj)


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


class AggregateOperation(DatabaseOperation):
    """Aggregation framework: DB operation wrapper"""

    def __init__(self, collection):
        self.collection = collection
        self.pipeline = []

    def apply(self, db):
        return db[self.collection].aggregate(
            self._get_pipeline_to_mongo())

    def _get_pipeline_to_mongo(self):
        return [to_mongo(i) for i in self.pipeline]

    def to_mongo(self):
        return {
            'aggregate': self.collection,
            'pipeline': self._get_pipeline_to_mongo(),
        }


class AggregateCmdProject(object):
    """Aggregation framework: $project command"""

    def __init__(self, args):
        self._args = args

    def to_mongo(self):
        ## Named expressions are just squashed in the same dict.
        ## Any previously defined project: will be overridden.
        ## todo: should we merge instead?
        projection = dict(
            (to_mongo(item.name), to_mongo(item.expression))
            for item in self._args)
        return {'$project': projection}


class Symbol(object):
    """Used to represent generic symbols"""

    def __init__(self, name):
        self.name = name

    def to_mongo(self):
        return self.name  # Name is used as-is..


class Map(dict):
    """Wrapper around dict, allowing to_mongo() serialization"""

    def to_mongo(self):
        return dict((key, to_mongo(val)) for key, val in self.iteritems())


class Expression(object):
    """Common base for expressions"""
    pass


class NamedExpression(Expression):
    def __init__(self, name, expression):
        self.name = name
        assert isinstance(self.name, basestring)
        self.expression = expression

    def to_mongo(self):
        return {self.name: to_mongo(self.expression)}


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


class LogicalOperationBase(OperationBase):
    def __init__(self, *expressions):
        self._expressions = []
        for expr in expressions:
            self.append(expr)

    def append(self, expr):
        if isinstance(expr, self.__class__):
            ## We should merge this one.
            for e in expr._expressions:
                self.append(e)
        else:
            self._expressions.append(expr)

    def _expressions_to_mongo(self):
        return [to_mongo(e) for e in self._expressions]

    def __repr__(self):
        return "{0}({1})".format(
            self.__class__.__name__,
            ', '.join(repr(x) for x in self._expressions))


class LogicalAnd(LogicalOperationBase):
    def to_mongo(self):
        return {'$and': self._expressions_to_mongo()}


class LogicalOr(LogicalOperationBase):
    def to_mongo(self):
        return {'$or': self._expressions_to_mongo()}


class LogicalNot(object):
    def __init__(self, expression):
        self._expression = expression

    def to_mongo(self):
        return {'$not': to_mongo(self._expression)}

    def __repr__(self):
        return "{0}({1})".format(
            self.__class__.__name__,
            repr(self._expression))


class FunctionCall(Expression):
    """
    Wrapper for function calls.
    This is kinda delicate, but should work..

    func(a, b, c) -> {'$func': [a, b, c]}
    """

    def __init__(self, function, args):
        self.function = function
        self.args = args

    def to_mongo(self):
        return {
            '${0}'.format(self.function): [
                to_mongo(a) for a in self.args
            ]
        }

    def __repr__(self):
        return "{0}({1})".format(
            self.function,
            ', '.join(repr(x) for x in self.args))
