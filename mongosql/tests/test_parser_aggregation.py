"""
Tests for the Aggregation framework
"""

from mongosql import parse
from mongosql.support import AggregateOperation


def test_aggregation_project_fields():
    result = parse('AGGREGATE article PROJECT title = 1, author = 1')
    assert isinstance(result, AggregateOperation)
    assert result.collection == 'article'
    assert result.to_mongo()['pipeline'] == [
        {'$project': {'title': 1, 'author': 1}}
    ]

    result = parse('AGGREGATE article PROJECT _id = 0, title = 1, author = 1')
    assert isinstance(result, AggregateOperation)
    assert result.collection == 'article'
    assert result.to_mongo()['pipeline'] == [
        {'$project': {'_id': 0, 'title': 1, 'author': 1}}
    ]


def test_aggregation_project_computed_field():
    result = parse(
        'AGGREGATE article PROJECT title = 1, '
        'doctoredPageViews = "$pageViews" + 10')
    assert isinstance(result, AggregateOperation)
    assert result.collection == 'article'
    assert result.to_mongo()['pipeline'] == [
        {'$project': {
            'title': 1,
            'doctoredPageViews': {
                '$add': ['$pageViews', 10],
            }}}]


def test_aggregation_project_rename_fields():
    result = parse("""
    AGGREGATE article
    PROJECT title = 1,
            page_views = '$pageViews',
            bar = '$other.foo'
    """)
    assert isinstance(result, AggregateOperation)
    assert result.collection == 'article'
    assert result.to_mongo()['pipeline'] == [
        {'$project': {
            'title': 1,
            'page_views': '$pageViews',
            'bar': '$other.foo',
        }}]


def test_aggregation_project_subdocument():
    result = parse("""
    AGGREGATE article
    PROJECT title = 1,
            stats = {
                pv = '$pageViews',
                foo = '$other.foo',
                dpv = '$pageViews' + 10,
            }
    """)
    assert isinstance(result, AggregateOperation)
    assert result.collection == 'article'
    assert result.to_mongo()['pipeline'] == [
        {'$project': {
            'title': 1,
            'stats': {
                'pv': "$pageViews",
                'foo': "$other.foo",
                'dpv': {'$add': ["$pageViews", 10]}
            },
        }}]
