import pika, sys, os, json


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbit"))
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
            body_dict = json.loads(body.decode("utf-8"))
            print(f"Message received: {body}", flush=True)

            if body_dict["operator"] == "+":
                body_dict["result"] = (
                    body_dict["operands"][0] + body_dict["operands"][1]
                )

            elif body_dict["operator"] == "-":
                body_dict["result"] = (
                    body_dict["operands"][0] - body_dict["operands"][1]
                )

            elif body_dict["operator"] == "*":
                body_dict["result"] = (
                    body_dict["operands"][0] * body_dict["operands"][1]
                )

            elif body_dict["operator"] == "/":
                body_dict["result"] = (
                    body_dict["operands"][0] / body_dict["operands"][1]
                )

            # else:
            # add exception scenario
            else:
                has_error = True

            if has_error:
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

            else:
                ch.basic_ack(delivery_tag=method.delivery_tag)
                result_json = json.dumps(body_dict)

                ch.basic_publish(exchange="", routing_key="queue_B", body=result_json)
        except:
            print("except", flush=True)
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
