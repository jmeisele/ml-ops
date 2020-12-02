"""
Author: Jason Eisele
Date: December 2, 2020
Scope: Function to add message to RabbitMQ queue
"""
import pika
from loguru import logger

def add_message_to_queue(body):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq-server', port=5672))
    channel = connection.channel()
    channel.queue_declare(queue='predictions')
    channel.basic_publish(exchange='', routing_key='predictions', body=body)
    logger.info(f"Sent {body} to message queue")
    connection.close()