"""
Author: Jason Eisele
Date: February 16, 2021
Scope: Function to add message to RabbitMQ queue
"""
import pika
from loguru import logger


def add_message_to_queue(body):
    credentials = pika.PlainCredentials('producer', 'producer')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(credentials=credentials,
                                  host='rabbitmq',
                                  port=5672)
    )
    channel = connection.channel()
    channel.queue_declare(queue='predictions', durable=True)
    channel.basic_publish(exchange='', routing_key='predictions', body=body)
    logger.info(f"Sent {body} to message queue")
    connection.close()


# def add_message_to_queue(queue, exchange, body):
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
#     channel = connection.channel()
#     channel.queue_declare(queue='hello')
#     channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
#     print(" [x] Sent 'Hello World!'")
#     connection.close()
