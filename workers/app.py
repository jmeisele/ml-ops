"""
Author: Jason Eisele
Date: December 2, 2020
Scope: Main app controller for workers
"""
from tasks import callback, insert_record

import pika
from loguru import logger

credentials = pika.PlainCredentials('consumer', 'consumer')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(credentials=credentials,
                              host='rabbitmq',
                              port=5672)
)

channel = connection.channel()

channel.queue_declare(queue='predictions', durable=True)
# channel.basic_consume(queue='predictions',
#                       on_message_callback=callback,
#                       auto_ack=True)
channel.basic_consume(queue='predictions',
                      on_message_callback=insert_record,
                      auto_ack=True)
# Remove auto_ack=True flag
# to ensure proper message acknowledgements

if __name__ == '__main__':
    logger.info('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
