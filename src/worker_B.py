import pika, sys, os
from pymongo import MongoClient
import json


def main():
    def callback(ch, method, properties, body):
        body = body.decode("utf-8")
        body = json.loads(body)
        print(f"Message received: {body}", flush=True)

        # worker_B publish the message to mongodb
        collection.insert_one(body)

    ## add logic to do the operant
    ## remove gateway connection and use service name instead

    # Mongodb connection
    client = MongoClient(host="mongodb")
    collection = client["test_db"]["test_collection"]

    # RabbitMQ connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbit"))
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
