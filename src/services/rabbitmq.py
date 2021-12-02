from enum import auto
from typing import Callable

import pika


class RabbitMQ:
    def __init__(self, user, password, host, port):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.uri = f"amqp://{self.user}:{self.password}@{self.host}:{self.port}"

        self.connect_rabbit()

    def connect_rabbit(self):
        self.connection = pika.BlockingConnection(pika.URLParameters(self.uri))
        self.channel = self.connection.channel()

    def exchange_declare(self, exchange: str, exchange_type: str):
        self.channel.exchange_declare(
            exchange=exchange, exchange_type=exchange_type
        )

    def queue_declare(self, queue: str, arguments: dict = {}):
        self.channel.queue_declare(queue=queue, arguments=arguments)

    def bind_queue_to_exchange(
        self, queue: str, exchange: str, routing_key: str
    ):
        self.channel.queue_bind(
            queue=queue, exchange=exchange, routing_key=routing_key
        )

    def basic_ack(self, delivery_tag: int):
        self.channel.basic_ack(delivery_tag=delivery_tag)

    def basic_nack(self, delivery_tag: int, requeue: bool):
        self.channel.basic_nack(delivery_tag=delivery_tag, requeue=requeue)

    def publish_to_queue(
        self, exchange: str, routing_key: str, body: object, properties: object
    ):
        self.channel.basic_publish(
            exchange=exchange, routing_key=routing_key, body=body, properties=properties
        )

    def retry_same_queue(self, queue:str,body: object, properties:object, delivery_tag:int):
        self.basic_ack(delivery_tag=delivery_tag)
        self.publish_to_queue(exchange="", routing_key=queue, body=body, properties=properties)

        print(f'Retry count: {properties.headers["x-death-count"]}', flush=True)

        
    


    def consume(
        self,
        queue: str,
        callback: Callable[
            [
                pika.channel.Channel,
                pika.spec.Basic.Deliver,
                pika.spec.BasicProperties,
                bytes,
            ],
            None,
        ],
        auto_ack: bool,
    ):
        self.channel.basic_consume(
            queue=queue, on_message_callback=callback, auto_ack=auto_ack
        )
        self.channel.start_consuming()


    def stop_consume(self):
        self.channel.stop_consuming()
