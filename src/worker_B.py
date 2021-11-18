import pika, sys, os
import pymongo
def main():
    host = '172.17.0.1'
    port = '5672'
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
    channel = connection.channel()
    

    channel.queue_declare(queue='queue_B')

    def callback(ch, method, properties, body):
        print(f'Message received: {body.decode("utf-8")}',flush=True)

        # worker_B publish the message to mongodb

 

    channel.basic_consume(queue='queue_B', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages from worker_A. To exit press CTRL+C')
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