#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='notifications',
                         type='direct')

receiver_id = sys.argv[1:] or 'my-id'

message = 'Hello World! ->'+receiver_id

channel.basic_publish(exchange='notifications',
                      routing_key=receiver_id,
                      body=message)

print " [x] Sent %r" % (message,)
connection.close()