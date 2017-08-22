#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

import watchdog
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from logger import log


class ChangeHandler(PatternMatchingEventHandler):
    def __init__(self, dir: str, filename: str, is_glob: bool):
        ext = os.path.splitext(filename)[1]
        super(ChangeHandler, self).__init__(patterns=["*%s" % ext])
        self.file_path = os.path.join(dir, filename)  # type: str
        self.modified = False  # type: bool
        self.is_glob = is_glob

    def on_created(self, event: watchdog.events.FileCreatedEvent):
        log.d("  on_created %s" % event.src_path)
        if self.is_glob or event.src_path != self.file_path:
            return
        self.modified = True

    def on_modified(self, event: watchdog.events.FileModifiedEvent):
        log.d("  on_modified %s" % event.src_path)
        if self.is_glob or event.src_path != self.file_path:
            return
        self.modified = True


def file(dirname, filename, timeout):
    """
    Wait until a file created.
    :param str dirname: Directory path to be watched.
    :param str filename: File name to be watched.
    :param num timeout: How many seconds to be wait. [sec]
    :return: Is created the file.
    :rtype bool
    """
    is_glob = filename.find('*') >= 0
    handler = ChangeHandler(dirname, filename, is_glob)
    observer = Observer()
    observer.schedule(handler, dirname, recursive=False)
    observer.start()

    try:
        UPDATE_INTERVAL = 0.5
        interval = UPDATE_INTERVAL
        while interval >= 0 and timeout > 0:
            time.sleep(0.1)
            timeout -= 0.1
            interval -= 0.1
            log.d('- time out remain %.2f, update interval %.2f' % (timeout, interval))
            if handler.modified is True:
                log.i('- now writing... %s ' % filename)
                handler.modified = False
                interval = UPDATE_INTERVAL

    except KeyboardInterrupt:
        observer.stop()

    if not is_glob:
        is_exists = os.path.exists(os.path.join(dirname, filename))
        if is_exists:
            if timeout <= 0:
                log.w("- The file still updating.")
        else:
            log.i("- time out")
            return False

    observer.stop()
    observer.join(timeout)

    return True
