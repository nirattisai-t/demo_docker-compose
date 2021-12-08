import pika, sys, os
from pika.spec import PORT
import json
import logging

from services.rabbitmq import RabbitMQ
from services.mongodb import MongoDB

# logging.basicConfig(filename = "worker_B.log", level=logging.INFO, format="%(levelname)s:%(message)s")
logFormatter = logging.Formatter("%(levelname)s:%(message)s")
logger = logging.getLogger("worker_B")
logger.setLevel(logging.INFO)


fileHandler = logging.FileHandler("worker_B.log")
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

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
            logger.info(f"Message received: {message_dict}")

            # worker_B publish the message to mongodb
            test_collection = mongo.get_collection("test_db", "test_collection")
            mongo.insert_document(test_collection, message_dict)
            rabbit.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logger.error(f"Found exception in callback : {e}")
            rabbit.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    logger.info(" [*] Waiting for messages from worker_A")
    rabbit.consume(queue="queue_B", callback=callback, auto_ack=False)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
