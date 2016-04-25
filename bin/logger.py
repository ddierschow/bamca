#!/usr/local/bin/python

import datetime, os, sys
import logging
import logging.config
import config

crawlers = [  # precluded from normal url tracking
    'DoCoMo/2.0 N905i(c100;TB;W24H16) (compatible; Googlebot-Mobile/2.1; +http://www.google.com/bot.html)',
    'Java/1.6.0_04',
    'Java/1.8.0_40',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/8.0.2 Safari/600.2.5 (Applebot/0.1; +http://www.apple.com/go/applebot)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6 - James BOT - WebCrawler http://cognitiveseo.com/bot.html',
    'Mozilla/5.0 (compatible; AhrefsBot/5.0; +http://ahrefs.com/robot/)',
    'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
    'Mozilla/5.0 (compatible; Cliqzbot/1.0 +http://cliqz.com/company/cliqzbot)',
    'Mozilla/5.0 (compatible; DotBot/1.1; http://www.opensiteexplorer.org/dotbot, help@moz.com)',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; Linux x86_64; Mail.RU_Bot/2.0; +http://go.mail.ru/help/robots)',
    'Mozilla/5.0 (compatible; MJ12bot/v1.4.5; http://www.majestic12.co.uk/bot.php?+)',
    'Mozilla/5.0 (compatible; MegaIndex.ru/2.0; +http://megaindex.com/crawler)',
    'Mozilla/5.0 (compatible; SemrushBot/0.99~bl; +http://www.semrush.com/bot.html)',
    'Mozilla/5.0 (compatible; SeznamBot/3.2-test1; +http://fulltext.sblog.cz/)',
    'Mozilla/5.0 (compatible; SeznamBot/3.2; +http://fulltext.sblog.cz/)',
    'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
    'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
    'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
    'Mozilla/5.0 (compatible; linkdexbot/2.0; +http://www.linkdex.com/bots/)',
    'Mozilla/5.0 (compatible; linkdexbot/2.2; +http://www.linkdex.com/bots/)',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53 (compatible; bingbot/2.0;  http://www.bing.com/bingbot.htm)',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'SAMSUNG-SGH-E250/1.0 Profile/MIDP-2.0 Configuration/CLDC-1.1 UP.Browser/6.2.3.3.c.1.101 (GUI) MMP/2.0 (compatible; Googlebot-Mobile/2.1; +http://www.google.com/bot.html)',
    'SafeAds.xyz bot',
    'bhcBot',
    'ia_archiver',
    'linkapediabot (+http://www.linkapedia.com)',
    'tbot-nutch/Nutch-1.10',
    'webcrawler101/Nutch-1.9',
]

# you were looking for pretty?  hah.
class Logger(object):
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
