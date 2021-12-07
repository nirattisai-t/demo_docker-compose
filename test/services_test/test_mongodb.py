from unittest.mock import MagicMock, patch
from pika import connection
from src.services.mongodb import MongoDB

from nose.tools import assert_equal


class TestMongoDB:
    @patch("src.services.mongodb.MongoDB.connect_to_mongo")
    def test_create_mongo_and_connect_to_database(self, mock_connection):
        _ = MongoDB("test_user", "test_password", "host", 8888)
        mock_connection.assert_called_once()

    def test_get_collection(self):
        mock_mongodb = MagicMock()
        collection = MagicMock()

        mongodb = MongoDB("test_user", "test_password", "host", 8888)
        mongodb.connection = MagicMock()

        mongodb.connection = {"test_database": {"test_collection": collection}}
        mock_mongodb.connection = {"test_database": {"test_collection": collection}}

        expected_result = mongodb.get_collection("test_database", "test_collection")
        actual_result = mock_mongodb.connection["test_database"]["test_collection"]

        assert_equal(expected_result, actual_result)

    def test_insert_document(self):
        mock_document = MagicMock()
        collection = MagicMock()
        collection.insert_one = MagicMock()

        mongodb = MongoDB("test_user", "test_password", "host", 8888)
        mongodb.insert_document(collection, mock_document)

        collection.insert_one.assert_called_once_with(mock_document)
