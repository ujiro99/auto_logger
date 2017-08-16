#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import threading
import time
from unittest import TestCase

from logger import watch


class WriteThread(threading.Thread):
    def __init__(self, filepath, cycle, sleep_time):
        super(WriteThread, self).__init__()
        self.stop_event = threading.Event()
        self.filepath = filepath
        self.cycle = cycle
        self.time = sleep_time

    def run(self):
        f = open(self.filepath, "w")
        print(" === start sub thread (sub class) === ")
        for i in range(self.cycle):
            time.sleep(self.time)
            f.write("%d\n" % i)
            f.flush()
            print("write line: %d" % i)
            if self.stop_event.is_set():
                break
        print(" === end sub thread (sub class) === ")
        f.close()

    def stop(self):
        os.remove(self.filepath)
        self.stop_event.set()


class TestFile(TestCase):
    def test_file(self):
        wd = os.getcwd()

        path = wd
        filename = 'test.tar.gz'
        timeout = 10
        w = WriteThread(os.path.join(wd, filename), 10, 0.1)
        w.start()
        is_created = watch.file(path, filename, timeout)
        w.stop()
        w.join()
        self.assertTrue(is_created)

    def test_file__timeout(self):
        path = "./"
        filename = "test.tar.gz"
        timeout = 0.1
        is_created = watch.file(path, filename, timeout)
        self.assertFalse(is_created)
