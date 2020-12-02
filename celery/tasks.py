"""
Author: Jason Eisele
Date: December 2, 2020
Scope: Celery worker tasks defined
"""
from .celery import app

@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)