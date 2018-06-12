import sys
import json
import logging
import pika

from config import SOCKET as sk

class RabbitQueue:
    def __init__(self, routing_key):
        self.logger = logging.getLogger("rabbit")
        self.routing_key = routing_key

    def connect(self):
        credentials = pika.PlainCredentials(sk["USER"], sk["PASSWD"])
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(sk["HOST"],sk["PORT"],'/',credentials))
        self.channel = self.connection.channel()
        self.queue = self.channel.queue_declare(queue= self.routing_key)

    def push(self, message):
        self.logger.debug("Function: RabbitQueue.push(%s), message: '%s'."%(self.routing_key, message))
        try:
            self.connect()
        except Exception as e:
            self.logger.error("Function: RabbitQueue.push '%s'."%(str(e)))
            try:
                self.connection.close()
            except Exception as e:
                pass
            return False
        self.channel.basic_publish(exchange='',
            routing_key = self.routing_key,
            properties=pika.BasicProperties(delivery_mode=2,),
            body = message)
        self.connection.close()
        return True

    def get(self, no_ack = True):
        self.logger.debug("Function: RabbitQueue.get(%s), from queue get all messages."%(self.routing_key))
        try:
            self.connect()
        except Exception as e:
            self.logger.error("Function: RabbitQueue '%s'."%(str(e)))
            try:
                self.connection.close()
            except Exception as e:
                pass
            return None
        self.channel = self.connection.channel()
        result = []
        for i in range(self.queue.method.message_count):
            body = self.channel.basic_get(queue=self.routing_key, no_ack=no_ack) # get queue basic with single queue
            result.append(body)
        self.connection.close()
        return result

