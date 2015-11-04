#!/usr/local/bin/python

import datetime, os, sys
import logging
import logging.config
import config

# you were looking for pretty?  hah.
class Logger:
    def __init__(self):
	logdate = datetime.datetime.now().strftime('%Y%m')

	env = config.ENV
	LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'serious': {
            'format': '%(asctime)s [%(process)d] %(levelname)s ' + str(config.USER_ID) + ' %(filename)s:%(lineno)d - %(message)s',
        },
        'informational': {
            'format': '%(asctime)s %(levelname)s ' + str(config.USER_ID) + ' - %(message)s',
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
            'filename': '/home/bamca/logs/' + env + '.file.log',
        },
        'upload': {
            'level': os.environ.get('LOG_LEVEL', 'INFO'),
            'formatter': 'informational',
            'class': 'logging.FileHandler',
            'filename': '/home/bamca/logs/' + env + '.upload.log',
        },
        'url': {
            'level': os.environ.get('LOG_LEVEL', 'INFO'),
            'formatter': 'serious',
            'class': 'logging.FileHandler',
            'filename': '/home/bamca/logs/' + env + '.url' + logdate + '.log',
        },
        'dbq': {
            'level': os.environ.get('LOG_LEVEL', 'INFO'),
            'formatter': 'serious',
            'class': 'logging.FileHandler',
            'filename': '/home/bamca/logs/' + env + '.dbq' + logdate + '.log',
        },
        'bot': {
            'level': os.environ.get('LOG_LEVEL', 'INFO'),
            'formatter': 'serious',
            'class': 'logging.FileHandler',
            'filename': '/home/bamca/logs/' + env + '.bot' + logdate + '.log',
        },
        'activity': {
            'level': os.environ.get('LOG_LEVEL', 'INFO'),
            'formatter': 'serious',
            'class': 'logging.FileHandler',
            'filename': '/home/bamca/logs/' + env + '.act.log',
        },
        'count': {
            'level': os.environ.get('LOG_LEVEL', 'INFO'),
            'formatter': 'informational',
            'class': 'logging.FileHandler',
            'filename': '/home/bamca/logs/' + env + '.count.log',
        },
        'refer': {
            'level': os.environ.get('LOG_LEVEL', 'INFO'),
            'formatter': 'informational',
            'class': 'logging.FileHandler',
            'filename': '/home/bamca/logs/' + env + '.refer.log',
        },
        'debug': {
            'level': os.environ.get('LOG_LEVEL', 'INFO'),
            'formatter': 'serious',
            'class': 'logging.FileHandler',
            'filename': '/home/bamca/logs/' + env + '.debug.log',
        },
        'root': {
            'level': os.environ.get('LOG_LEVEL', 'INFO'),
            'formatter': 'serious',
            'class': 'logging.FileHandler',
            'filename': '/home/bamca/logs/' + env + '.root.log',
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
        'activity': {
            'level': 'INFO',
            'handlers': ['activity'],
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
    },
    'root': {
        'handlers': ['root'],
        'level': os.environ.get('LOG_LEVEL', 'DEBUG'),
    },
}

	logging.config.dictConfig(LOGGING)

        self.console	= logging.getLogger('console')
        self.file	= logging.getLogger('file')
        self.upload	= logging.getLogger('upload')
        self.url	= logging.getLogger('url')
        self.dbq	= logging.getLogger('dbq')
        self.bot	= logging.getLogger('bot')
        self.activity	= logging.getLogger('activity')
        self.count	= logging.getLogger('count')
        self.refer	= logging.getLogger('refer')
        self.debug	= logging.getLogger('debug')
	self.root	= logging.getLogger('root')
