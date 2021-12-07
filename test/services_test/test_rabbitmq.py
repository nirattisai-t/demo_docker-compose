from unittest.mock import MagicMock, patch
from pika import connection
from src.services.rabbitmq import RabbitMQ


class TestRabbitMQ:
    @patch("src.services.rabbitmq.RabbitMQ.connect_rabbit")
    def test_connect_rabbit(self, mock_connect_rabbit):
        _ = RabbitMQ("user", "pass", "host", 5678)
        mock_connect_rabbit.assert_called_once()
