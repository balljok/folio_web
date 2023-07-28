import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging(filename='log.log', level='ERROR'):
    if os.path.isdir('./logs'):
        log_location = './logs/'
    else:
        log_location = './'

    log_file = log_location + filename

    if level == 'DEBUG':
        level = logging.DEBUG
    elif level == 'INFO':
        level = logging.INFO
    elif level == 'WARNING':
        level = logging.WARNING
    elif level == 'ERROR':
        level = logging.ERROR
    elif level == 'CRITICAL':
        level = logging.CRITICAL
    else:
        level = logging.ERROR

    logging.basicConfig(
        handlers=[RotatingFileHandler(
            log_file, mode='a', maxBytes=5*1024*1024, backupCount=2, encoding=None, delay=0)],
        level=level,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt='%Y-%m-%dT%H:%M:%S')