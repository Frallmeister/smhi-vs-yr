import logging.config

DEFAULT_LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            'class': 'logging.Formatter',
            'format': '%(asctime)s: %(levelname)s: %(filename)s: Line %(lineno)d: %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S"
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'default'
        },
        'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'logfile.log',
                'maxBytes': 1024*1024,
                'backupCount': 10,
                'formatter': 'default',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        }
    }
}


def configure_logging():
    logging.config.dictConfig(DEFAULT_LOGGING)