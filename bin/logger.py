#!/usr/local/bin/python

import datetime
import os
import logging
import logging.config
import config


# you were looking for pretty?  hah.
class Logger(object):
    def __init__(self):
        logdate = datetime.datetime.now().strftime('%Y%m')
        logging_config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'single': {
                    'format': '%(asctime)s [%(process)d] %(levelname)s {} - %(message)s'.format(config.USER_ID),
                    'style': '%',
                },
                'serious': {
                    'format': '%(asctime)s [%(process)d] %(levelname)s {} %(filename)s:%(lineno)d - %(message)s'.format(
                        config.USER_ID),
                    'style': '%',
                },
                'informational': {
                    'format': '%(asctime)s %(levelname)s {} - %(message)s'.format(config.USER_ID),
                    'style': '%',
                },
            },
            'handlers': {
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                    'formatter': 'informational'
                },
                'file': {
                    'level': os.environ.get('LOG_LEVEL', 'INFO'),
                    'formatter': 'informational',
                    'class': 'logging.FileHandler',
                    'filename': '/home/bamca/logs/' + config.ENV + '.file.log',
                },
                'upload': {
                    'level': os.environ.get('LOG_LEVEL', 'INFO'),
                    'formatter': 'informational',
                    'class': 'logging.FileHandler',
                    'filename': '/home/bamca/logs/' + config.ENV + '.upload.log',
                },
                'exc': {
                    'level': os.environ.get('LOG_LEVEL', 'INFO'),
                    'formatter': 'single',
                    'class': 'logging.FileHandler',
                    'filename': '/home/bamca/logs/' + config.ENV + '.exc' + logdate + '.log',
                },
                'url': {
                    'level': os.environ.get('LOG_LEVEL', 'INFO'),
                    'formatter': 'single',
                    'class': 'logging.FileHandler',
                    'filename': '/home/bamca/logs/' + config.ENV + '.url' + logdate + '.log',
                },
                'dbq': {
                    'level': os.environ.get('LOG_LEVEL', 'INFO'),
                    'formatter': 'single',
                    'class': 'logging.FileHandler',
                    'filename': '/home/bamca/logs/' + config.ENV + '.dbq' + logdate + '.log',
                },
                'bot': {
                    'level': os.environ.get('LOG_LEVEL', 'INFO'),
                    'formatter': 'serious',
                    'class': 'logging.FileHandler',
                    'filename': '/home/bamca/logs/' + config.ENV + '.bot' + logdate + '.log',
                },
                'count': {
                    'level': os.environ.get('LOG_LEVEL', 'INFO'),
                    'formatter': 'informational',
                    'class': 'logging.FileHandler',
                    'filename': '/home/bamca/logs/' + config.ENV + '.count' + logdate + '.log',
                },
                'refer': {
                    'level': os.environ.get('LOG_LEVEL', 'INFO'),
                    'formatter': 'informational',
                    'class': 'logging.FileHandler',
                    'filename': '/home/bamca/logs/' + config.ENV + '.refer.log',
                },
                'debug': {
                    'level': os.environ.get('LOG_LEVEL', 'INFO'),
                    'formatter': 'serious',
                    'class': 'logging.FileHandler',
                    'filename': '/home/bamca/logs/' + config.ENV + '.debug.log',
                },
                'root': {
                    'level': os.environ.get('LOG_LEVEL', 'INFO'),
                    'formatter': 'serious',
                    'class': 'logging.FileHandler',
                    'filename': '/home/bamca/logs/' + config.ENV + '.root.log',
                },
                'devnull': {
                    'level': 'CRITICAL',
                    'formatter': 'serious',
                    'class': 'logging.FileHandler',
                    'filename': '/dev/null',
                },
            },
            'loggers': {
                'console': {
                    'level': 'DEBUG',
                    'handlers': ['console'],
                    'propagate': False,
                },
                'file': {
                    'level': 'INFO',
                    'handlers': ['file'],
                    'propagate': False,
                },
                'upload': {
                    'level': 'INFO',
                    'handlers': ['upload'],
                    'propagate': False,
                },
                'exc': {
                    'level': 'INFO',
                    'handlers': ['exc'],
                    'propagate': False,
                },
                'url': {
                    'level': 'INFO',
                    'handlers': ['url'],
                    'propagate': False,
                },
                'dbq': {
                    'level': 'INFO',
                    'handlers': ['dbq'],
                    'propagate': False,
                },
                'bot': {
                    'level': 'INFO',
                    'handlers': ['bot'],
                    'propagate': False,
                },
                'count': {
                    'level': 'INFO',
                    'handlers': ['count'],
                    'propagate': False,
                },
                'refer': {
                    'level': 'INFO',
                    'handlers': ['refer'],
                    'propagate': False,
                },
                'debug': {
                    'level': 'INFO',
                    'handlers': ['debug'],
                    'propagate': False,
                },
                'devnull': {
                    'level': 'CRITICAL',
                    'handlers': ['devnull'],
                    'propagate': False,
                },
            },
            'root': {
                'handlers': ['root'],
                'level': os.environ.get('LOG_LEVEL', 'DEBUG'),
            },
        }

        logging.config.dictConfig(logging_config)

        self.console = logging.getLogger('console')
        self.file = logging.getLogger('file')
        self.upload = logging.getLogger('upload')
        self.exc = logging.getLogger('exc')
        self.url = logging.getLogger('url')
        self.dbq = logging.getLogger('dbq')
        self.bot = logging.getLogger('bot')
        self.count = logging.getLogger('count')
        self.refer = logging.getLogger('refer')
        self.debug = logging.getLogger('debug')
        self.root = logging.getLogger('root')
        self.devnull = logging.getLogger('devnull')
