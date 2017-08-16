import logging
from logging import getLogger, StreamHandler

handler = StreamHandler()
handler.setLevel(logging.INFO)

logger = getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False

def d(msg):
    """
    Debug log
    :param str | bytes msg: Message string.
    """
    if isinstance(msg, str):
        logger.debug(msg)
    elif isinstance(msg, bytes):
        logger.debug(msg.decode("utf-8"))

def i(msg):
    """
    Info log
    :param str msg: Message string.
    """
    logger.info(msg)

def w(msg):
    """
    Warning log
    :param str msg: Message string.
    """
    logger.warning(msg)

def e(msg):
    """
    Error log
    :param str msg: Message string.
    """
    logger.error(msg)
