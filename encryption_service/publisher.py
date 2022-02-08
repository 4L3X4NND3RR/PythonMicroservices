import logging
import time
from pika.exceptions import AMQPConnectionError
import os
import pika


class Publisher:
    def __init__(self) -> None:
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
                self._connection = pika.BlockingConnection(parameters=parameters)
                break
            except AMQPConnectionError:
                logging.error("Couldn't create a connection to Rabbitmq, retrying in 15 secs.")
                time.sleep(15)

        # Setup channel
        self._channel = self._connection.channel()

        # Setup Exchange
        self._channel.exchange_declare(
            exchange=os.getenv("RABBIT_EXCHANGE"), exchange_type="direct"
        )

    def publish(self, routing_key, message):
        self._channel.basic_publish(
            exchange=os.getenv("RABBIT_EXCHANGE"), routing_key=routing_key, body=message
        )

    def close_connection(self):
        self._connection.close()
