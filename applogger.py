import logging

__logger = None

def setup(logger, logpath):
    file_handler = logging.FileHandler(logpath)
    file_handler.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    __logger = logger

def info(message):
    if __logger != None:
        __logger.info(message)

def get_logger():
    return __logger
