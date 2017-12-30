#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import enum
import logging
from logging import StreamHandler

handler = StreamHandler()
logger = logging.getLogger(__name__)


class Level(enum.Enum):
    FATAL = logging.FATAL
    ERROR = logging.ERROR
    WARN = logging.WARN
    INFO = logging.INFO
    DEBUG = logging.DEBUG


class ColoredFormatter(logging.Formatter):
    RESET_SEQ = "\033[0m"
    COLOR_SEQ = "\033[1;%dm"
    COLOR_START = "COLOR_START"
    COLOR_END = "COLOR_END"
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
    COLORS = {
        'ERROR':   RED,
        'WARNING': YELLOW,
        'INFO':    WHITE,
        'DEBUG':   CYAN,
    }

    def __init__(self, fmt):
        """
        :param str fmt: Format string.
        """
        logging.Formatter.__init__(self, fmt)
        self.fmt = fmt.replace(ColoredFormatter.COLOR_END, ColoredFormatter.RESET_SEQ)

    def format(self, record):
        """
        Output colored log
        :param logging.LogRecord record:
        :return: Format result.
        :rtype str
        """
        levelname = record.levelname
        if levelname in ColoredFormatter.COLORS:
            cs = ColoredFormatter.COLOR_SEQ % (30 + ColoredFormatter.COLORS[levelname])
            fmt = self.fmt.replace(ColoredFormatter.COLOR_START, cs)
            # update color of format
            self._style._fmt = fmt

        return logging.Formatter.format(self, record)


def init():
    """
    Initialize log module.
    """
    handler.setLevel(logging.INFO)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False
    f = ColoredFormatter("COLOR_START%(message)sCOLOR_END")
    handler.setFormatter(f)


def set_level(level: Level):
    """
    Set logging level
    :param Level level: Log level
    """
    logger.setLevel(level.value)
    handler.setLevel(level.value)
    if level == Level.DEBUG:
        f = ColoredFormatter("COLOR_START%(asctime)s %(levelname)-7sCOLOR_END %(message)s")
        f.default_time_format = '%H:%M:%S'
        f.default_msec_format = '%s.%03d'
        handler.setFormatter(f)


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
