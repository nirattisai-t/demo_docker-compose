import pika, sys, os

from pika.spec import PORT

import json

from services.rabbitmq import RabbitMQ
from services.mongodb import MongoDB


## Get environment variables
MONGO_USER = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASS = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
MONGO_HOST = os.getenv("MONGODB_HOST")
MONGO_PORT = os.getenv("MONGODB_PORT")
RABBIT_USER = os.getenv("RABBITMQ_DEFAULT_USER")
RABBIT_PASS = os.getenv("RABBITMQ_DEFAULT_PASSWORD")
RABBIT_HOST = os.getenv("RABBITMQ_HOST")
RABBIT_PORT = os.getenv("RABBITMQ_PORT")

mongo = MongoDB(MONGO_USER, MONGO_PASS, MONGO_HOST, MONGO_PORT)
rabbit = RabbitMQ(RABBIT_USER, RABBIT_PASS, RABBIT_HOST, RABBIT_PORT)

rabbit.queue_declare(queue="queue_B")

def main():
 
    def callback(ch, method, properties, body):
        try:
            message_dict = json.loads(body.decode("utf-8"))
            print(f"Message received: {message_dict}", flush=True)

            # worker_B publish the message to mongodb
            mongo.insert_document("test_db", "test_collection", message_dict)
            rabbit.basic_ack(delivery_tag = method.delivery_tag)
        except Exception as e:
            print(f"Found exception in callback : {e}", flush=True)
            rabbit.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            

   


    print(" [*] Waiting for messages from worker_A. To exit press CTRL+C")
    rabbit.consume(queue="queue_B", callback=callback, auto_ack=False)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
