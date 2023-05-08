import logging
import logging.config


class Logger:

    @staticmethod
    def get(name, filename=None, logformat="%(levelname)s - %(message)s", loglevel='INFO'):

        default_handlers = ['streamHandler']

        if filename:
            file_handler = {
                'class': 'logging.FileHandler',
                'formatter': 'baseFormatter',
                'filename': filename,
            }
            default_handlers.append('fileHandler')
        else:
            file_handler = None

        log_config = {
            'version': 1,
            'handlers': {
                'fileHandler': file_handler,
                'streamHandler': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'baseFormatter',
                },
            },
            'loggers': {
                name: {
                    'handlers': default_handlers,
                    'level': loglevel,
                },
            },
            'formatters': {
                'baseFormatter': {
                    'format': logformat
                },
            },
        }

        logging.config.dictConfig(log_config)
        return logging.getLogger(name)
