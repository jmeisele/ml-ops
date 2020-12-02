"""
Author: Jason Eisele
Date: December 2, 2020
Scope: Main app controller for celery workers
"""
from celery import Celery

app = Celery('celery',
             broker='amqp://rabbitmq:5672',
            #  backend='amqp://',
             include=['celery.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
