import sys, os, json, logging
from utils.calculator_utils import calculate, check_invalid_operator, check_invalid_operands
from services.rabbitmq import RabbitMQ


logFormatter = logging.Formatter("%(levelname)s:%(message)s")
logger = logging.getLogger("worker_A")
logger.setLevel(logging.INFO)


fileHandler = logging.FileHandler("worker_A.log")
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)



## Get environment variables
RABBIT_USER = os.getenv("RABBITMQ_DEFAULT_USER")
RABBIT_PASS = os.getenv("RABBITMQ_DEFAULT_PASSWORD")
RABBIT_HOST = os.getenv("RABBITMQ_HOST")
RABBIT_PORT = os.getenv("RABBITMQ_PORT")

rabbit = RabbitMQ(RABBIT_USER, RABBIT_PASS, RABBIT_HOST, RABBIT_PORT)
rabbit.exchange_declare(exchange="dlx", exchange_type="direct")

rabbit.queue_declare(
    queue="queue_A",
    arguments={
        "x-dead-letter-exchange": "dlx",
        "x-dead-letter-routing-key": "dlx_key",
    },
)
rabbit.queue_declare(queue="dl_queue")
rabbit.queue_declare(queue="queue_B")

rabbit.bind_queue_to_exchange(queue="dl_queue", exchange="dlx", routing_key="dlx_key")


def main():

    def callback(ch, method, properties, body):
        has_error = False
        # Calculate
        # {"operands":[int:x1, int:x2], "operator":"+"}
        # Assume 2 operands, if operator = "-" --> x1 - x2
        try:
            message_dict = json.loads(body.decode("utf-8"))
            logger.info(f"Message received: {body}")

            operator = message_dict["operator"]
            operands = message_dict["operands"]

            has_error = check_invalid_operator(operator) or check_invalid_operands(
                operands
            )

            if not has_error:
                message_dict["result"] = calculate(operator, operands)
                rabbit.basic_ack(delivery_tag=method.delivery_tag)
                result_json = json.dumps(message_dict)

                rabbit.publish_to_queue(
                    exchange="",
                    routing_key="queue_B",
                    body=result_json,
                    properties=properties,
                )

            elif not properties.headers:
                properties.headers["x-death-count"] = 1
                rabbit.retry_same_queue(
                    queue="queue_A",
                    body=body,
                    properties=properties,
                    delivery_tag=method.delivery_tag,
                )
                # rabbit.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
                logger.info(f'Retry count: {properties.headers["x-death-count"]}')


            elif properties.headers["x-death-count"] < 3:
                properties.headers["x-death-count"] += 1
                rabbit.retry_same_queue(
                    queue="queue_A",
                    body=body,
                    properties=properties,
                    delivery_tag=method.delivery_tag,
                )
                # rabbit.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
                logger.info(f'Retry count: {properties.headers["x-death-count"]}')

            else:
                # Check that if requeue = True, message gose to both dl_q and q_A or just q_A
                rabbit.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                logger.warning(
                    "Retry failed: The message is published to Death-Letter"
                )

        except Exception as e:
            logger.error(f"Found exception : {e}")
            rabbit.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    rabbit.consume(queue="queue_A", callback=callback, auto_ack=False)
    logger.info(" [*] Waiting for messages from queue_A")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
