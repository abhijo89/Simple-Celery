#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import socket

__author__ = "UniCourt India"
__version__ = "v2.2018.03.26"

import celery
import raven
import sys
from raven.contrib.celery import register_signal, register_logger_signal

config_dict = {
            'beat_scheduler': 'restapp.utils.celery.schedulers.DatabaseScheduler',
            'beat_max_loop_interval': 2,
            'imports': [],
            'broker_url': 'amqp://codaxtr_user:c0d@xtr@{0}:{1}/{2}'.format('192.168.2.5', 'x', 'y'),

            'result_backend': 'test_bk',
            'result_serializer': "json",

            'task_routes': [],
            'task_queues': [],
            'task_default_routing_key': 'researcher.default',
            'task_default_exchange': 'researcher',
            'task_default_queue': 'researcher_default'
}

class Celery(celery.Celery):

    def on_configure(self):
        client = raven.Client(
            dsn='https://8e730adbb30c465eb9ae38042397db0e:691c34364d634327baf865fc3ec6f139@sentry.io/623551',
            release='v1.0.1',
            environment=sys.env.get('instance_info', 'instance_type').lower(),
            name=socket.gethostname(),

        )
        register_logger_signal(client, loglevel=30)

        register_signal(client)

app = Celery(__name__)
app.config_from_object(config_dict)