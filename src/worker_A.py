import pika, sys, os

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='queue_A')
    channel.queue_declare(queue='queue_B')


    def callback(ch, method, properties, body):
        ch.basic_publish(exchange='', routing_key='queue_B', body=body)
        print(f'Message received: {body.decode("utf-8")}')

    channel.basic_consume(queue='queue_A', on_message_callback=callback, auto_ack=True)


    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)