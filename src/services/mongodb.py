import os

from pymongo import MongoClient 
from pymongo.collection import Collection as MongoCollection


class MongoDB:
    def __init__(self, user, password, host, port) -> None:
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.uri = f"mongodb://{self.user}:{self.password}@{self.host}:{self.port}"

        self.connect_to_mongo()

    def connect_to_mongo(self) -> None:
        self.connection = MongoClient(self.uri)

    # Fix Pylance return type warning
    def _get_collection(self, database: str, collection: str) -> MongoCollection:
        return self.connection[database][collection]

    def insert_document(self, database: str, collection: str, document: object) -> None:
        collection = self._get_collection(database=database, collection=collection)
        collection.insert_one(document)
