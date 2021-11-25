import pika, sys, os, json


def main():
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

    channel.exchange_declare(exchange="dlx", exchange_type="direct")

    channel.queue_declare(
        queue="queue_A",
        arguments={
            "x-dead-letter-exchange": "dlx",
            "x-dead-letter-routing-key": "dlx_key",
        },
    )
    channel.queue_declare(queue="queue_B")

    channel.queue_declare(queue="dl_queue")
    channel.queue_bind(queue="dl_queue", exchange="dlx", routing_key="dlx_key")

    def callback(ch, method, properties, body):
        has_error = False
        # Calculate
        # {"operands":[int:x1, int:x2], "operator":"+"}
        # Assume 2 operands, if operator = "-" --> x1 - x2
        try:
            message_dict = json.loads(body.decode("utf-8"))
            print(f"Message received: {body}", flush=True)

            if message_dict["operator"] == "+":
                message_dict["result"] = (
                    message_dict["operands"][0] + message_dict["operands"][1]
                )

            elif message_dict["operator"] == "-":
                message_dict["result"] = (
                    message_dict["operands"][0] - message_dict["operands"][1]
                )

            elif message_dict["operator"] == "*":
                message_dict["result"] = (
                    message_dict["operands"][0] * message_dict["operands"][1]
                )

            elif message_dict["operator"] == "/":
                message_dict["result"] = (
                    message_dict["operands"][0] / message_dict["operands"][1]
                )

            # else:
            # add exception scenario
            else:
                has_error = True

            if has_error:
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

            else:
                ch.basic_ack(delivery_tag=method.delivery_tag)
                result_json = json.dumps(message_dict)

                ch.basic_publish(exchange="", routing_key="queue_B", body=result_json)
        except Exception as e:
            print(f"Found exception : {e}", flush=True)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    channel.basic_consume(queue="queue_A", on_message_callback=callback, auto_ack=False)
    print(" [*] Waiting for messages. To exit press CTRL+C")
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
