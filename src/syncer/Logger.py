import logging

log_handler = logging.getLogger(__name__)
_DEFAULT_LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

_SHARED = None


class Logger:

    @staticmethod
    def debug(message):
        log_handler.info(message)


def configure_logging():
    log_handler.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()

    formatter = logging.Formatter(_DEFAULT_LOG_FORMAT, datefmt='%H:%M:%S',)
    ch.setFormatter(formatter)

    log_handler.addHandler(ch)
