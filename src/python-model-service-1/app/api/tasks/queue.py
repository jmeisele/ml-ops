"""
Author: Jason Eisele
Date: December 2, 2020
Scope: Function to add message to RabbitMQ queue
"""
import pika

def add_message_to_queue(queue, exchange, body):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    # channel.queue_declare(queue='hello')
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange='', routing_key='hello', body=body)
    print(" [x] Sent 'Hello World!'")
    connection.close()