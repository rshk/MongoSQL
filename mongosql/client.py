"""
Custom MongoClient
"""

from pymongo.mongo_client import MongoClient
from pymongo.database import Database

from mongosql import parse


class MongoSqlClient(MongoClient):
    def __getattr__(self, name):
        return MongoSqlDatabase(self, name)


class MongoSqlDatabase(Database):
    def sql(self, query):
        return parse(query).apply(self)
