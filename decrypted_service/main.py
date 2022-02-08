import logging
import os
import time
from dotenv import load_dotenv
import pika
from pika.exceptions import AMQPConnectionError

load_dotenv()

# Setup credentials
credentials = pika.PlainCredentials(
    os.getenv("RABBIT_USER"), os.getenv("RABBIT_PASSWORD")
)

# Setup connection
parameters = pika.ConnectionParameters(host=os.getenv("RABBIT_HOST"),
    port=5672, virtual_host=os.getenv("RABBIT_VHOST"), credentials=credentials
)

while True:
    try:
        connection = pika.BlockingConnection(parameters=parameters)
        break
    except AMQPConnectionError:
        logging.error("Couldn't create a connection to Rabbitmq, retrying in 15 secs.")
        time.sleep(15)


# Setup channel
channel = connection.channel()

# Setup Exchange
channel.exchange_declare(exchange=os.getenv("RABBIT_EXCHANGE"), exchange_type="direct")

# Setup Queue
result = channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue

# Binding queue with channel and exchange
channel.queue_bind(
    exchange=os.getenv("RABBIT_EXCHANGE"),
    queue=queue_name,
    routing_key=os.getenv("RABBIT_ROUTING_KEY"),
)

print(" [*] Waiting for decrypted words. To exit press CTRL+C")


# Handle message
def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


# Init channel
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
