import enum
import logging
from logging import getLogger, StreamHandler

handler = StreamHandler()
handler.setLevel(logging.INFO)

logger = getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False


class Level(enum.Enum):
    FATAL = logging.FATAL
    ERROR = logging.ERROR
    WARN  = logging.WARN
    INFO  = logging.INFO
    DEBUG = logging.DEBUG


def set_level(level: Level):
    """
    Set logging level
    :param Level level: Log level
    """
    logger.setLevel(level.value)
    handler.setLevel(level.value)

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
