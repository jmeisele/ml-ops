"""
Author: Jason Eisele
Date: December 2, 2020
Scope: Worker tasks defined
"""
from loguru import logger

def callback(ch, method, properties, body):
    logger.debug(f"Received body: {body}")
