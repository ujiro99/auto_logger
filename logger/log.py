import logging
from logging import getLogger, StreamHandler

handler = StreamHandler()
handler.setLevel(logging.INFO)

logger = getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False

logger.debug('hello')

def d(msg):
    logger.debug(msg)

def i(msg):
    logger.info(msg)

def w(msg):
    logger.warning(msg)

def e(msg):
    logger.error(msg)
