import pika, sys, os

from pika.spec import PORT
from pymongo import MongoClient
import json


def main():
    def callback(ch, method, properties, body):
        message_dict = json.loads(body.decode("utf-8"))
        print(f"Message received: {message_dict}", flush=True)

        # worker_B publish the message to mongodb
        collection.insert_one(message_dict)

    ## add logic to do the operant
    ## remove gateway connection and use service name instead

    # Mongodb connection
    MONGO_USER = os.getenv("MONGO_INITDB_ROOT_USERNAME")
    MONGO_PASS = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
    MONGO_HOST = os.getenv("MONGODB_HOST")
    MONGO_PORT = os.getenv("MONGODB_PORT")
    MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}"
    mongo_client = MongoClient(MONGO_URI)
    # mongo_client = MongoClient(
    #     host=MONGO_HOST, username=MONGO_USER, password=MONGO_PASS, port=int(MONGO_PORT)
    # )
    collection = mongo_client["test_db"]["test_collection"]

    # RabbitMQ connection
    RABBIT_USER = os.getenv("RABBITMQ_DEFAULT_USER")
    RABBIT_PASS = os.getenv("RABBITMQ_DEFAULT_PASSWORD")
    RABBIT_HOST = os.getenv("RABBITMQ_HOST")
    RABBIT_PORT = os.getenv("RABBITMQ_PORT")
    # RABBIT_URL = f"amqp://{RABBIT_USER}:{RABBIT_PASS}@{RABBIT_HOST}:{RABBIT_PORT}"
    # connection = pika.BlockingConnection(pika.URLParameters(RABBIT_URL))
    credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
    parameters = pika.ConnectionParameters(host=RABBIT_HOST, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue="queue_B")

    channel.basic_consume(queue="queue_B", on_message_callback=callback, auto_ack=True)

    print(" [*] Waiting for messages from worker_A. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
