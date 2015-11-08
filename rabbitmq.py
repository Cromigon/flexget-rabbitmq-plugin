#!/usr/bin/env python
from __future__ import unicode_literals, division, absolute_import
import logging
import base64
import pika

from flexget import plugin
from flexget.event import event
from flexget.utils.template import RenderError

log = logging.getLogger('pushbullet')

class OutputRabbitmq(object):
    """
    Example::

        rabbitmq:
            host: <HOST> (default: "localhost")
            port: <PORT> (default: 5672)
            username: <USERNAME> (default: "guest")
            password: <PASSWORD> (default: "guest")
            exchange: <EXCHANGE> (default: '')
            routing_key: <ROUTING_KEY>
            delivery_mode: <DELIVERY_MODE> (default: 2)
            queue_name: <QUEUE_NAME>
            queue_durable: <QUEUE_DURABLE> (default: True)
            body: <BODY> (default: "{{series_name}} {{series_id}}" -- accepts Jinja2)
    """
    default_body = ('{% if series_name is defined %}{{tvdb_series_name|d(series_name)}} {{series_id}} '
                    '{{tvdb_ep_name|d('')}}{% elif imdb_name is defined %}{{imdb_name}} '
                    '{{imdb_year}}{% else %}{{title}}{% endif %}')

    schema = {
        'type': 'object',
        'properties': {
            'host': {'type': 'string', 'default': 'localhost'},
            'port': {'type': 'integer', 'default': 5672},
            'username': {'type': 'string', 'default': 'guest'},
            'password': {'type': 'string', 'default': 'guest'},
            'exchange': {'type': 'string', 'default': ''},
            'routing_key': {'type': 'string'},
            'delivery_mode': {'type': 'integer', 'default': 2},
            'queue_name': {'type': 'string'},
            'queue_durable': {'type': 'boolean', 'default': True},
            'body': {'type': 'string', 'default': default_body}
        },
        'required': ['routing_key', 'queue_name'],
        'additionalProperties': False
    }

    @plugin.priority(0)
    def on_task_output(self, task, config):
        # FOR LOOP HERE
        for entry in task.accepted:
            body = config['body']
            try:
                message = entry.render(body)
            except RenderError as e:
                log.warning('Problem rendering `body`: %s' % e)
                message = "Download started!"

            self.send_message(task, message, config)

    def send_message(self, task, message, config):
        host = config['host']
        port = config['port']
        username = config['username']
        password = config['password']
        exchange = config['exchange']
        routing_key = config['routing_key']
        delivery_mode = config['delivery_mode']
        queue_name = config['queue_name']
        queue_durable = config['queue_durable']

        if task.options.test:
            log.info('Test mode. RabbitMQ notification would be:')
            log.info('    Host: %s' % host)
            log.info('    Port: %i' % port)
            log.info('    Username: %s' % username)
            log.info('    Password: %s' % password)
            log.info('    Routing Key: %s' % routing_key)
            log.info('    Delivery Mode: %s' % delivery_mode)
            log.info('    Queue name: %s' % queue_name)
            log.info('    Queue durable: %s' % queue_durable)
            log.info('    Body: %s' % message)
            return

        credentials = pika.PlainCredentials(username, password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=host, port=port, credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=queue_durable)

        channel.basic_publish(exchange=exchange,
                routing_key=routing_key,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode = delivery_mode,
                    ))
        connection.close()

@event('plugin.register')
def register_plugin():
    plugin.register(OutputRabbitmq, 'rabbitmq', api_ver=2)