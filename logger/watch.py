#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import watchdog
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


class ChangeHandler(PatternMatchingEventHandler):
    def __init__(self, patterns: list):
        super(ChangeHandler, self).__init__(patterns=patterns)
        self.file_name = None  # type: str
        self.finished = False  # type: bool

    def on_created(self, event: watchdog.events.FileCreatedEvent):
        print("  on_created %s" % event.src_path)
        if event.is_directory:
            return
        self.file_name = event.src_path
        # self.finished = True

    def on_modified(self, event: watchdog.events.FileModifiedEvent):
        print("  on_modified %s" % event.src_path)
        if event.is_directory:
            return
        self.file_name = event.src_path
        # self.finished = True


def file(path, extension, timeout):
    """
    Wait until a file created.
    :param str path: Directory path to be watched.
    :param str extension: File extension to be watched.
    :param num timeout: How many seconds to be wait. [sec]
    :return: Created file name.
    :rtype str
    """

    handler = ChangeHandler(["*." + extension])
    observer = Observer()
    observer.schedule(handler, path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(0.1)
            timeout -= 0.1
            if handler.finished is True:
                observer.stop()
                break
            elif timeout <= 0:
                observer.stop()
                print("- timeout")
                break
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

    return handler.file_name
