import os

CLOUDAMQP_URL = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost//')
