#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from threading import Thread
import time
from unittest import TestCase

from logger import watch, log


class WriteThread:
    def __init__(self, filepath, cycle, sleep_time):
        self.__stop = False
        self.filepath = filepath
        self.cycle = cycle
        self.time = sleep_time
        self.t = Thread(target=self.__write)

    def __write(self):
        log.d("=== start sub thread (sub class) === ")
        f = open(self.filepath, "w")
        for i in range(self.cycle):
            if self.__stop:
                log.d(" canceled")
                break
            time.sleep(self.time)
            f.write("%d\n" % i)
            f.flush()
            log.d(" write line: %d" % i)
        f.close()
        log.d("=== end sub thread (sub class) === ")

    def start(self):
        self.t.start()

    def stop(self):
        self.__stop = True
        self.t.join()
        os.remove(self.filepath)


class TestFile(TestCase):

    def test_file(self):
        log.set_level(log.Level.DEBUG)

        wd = os.getcwd()
        filename = 'test_file.tar.gz'
        w = WriteThread(os.path.join(wd, filename), 5, 0.1)
        w.start()
        timeout = 10
        is_created = watch.file(wd, filename, timeout)
        w.stop()
        self.assertTrue(is_created)

    def test_file__not_exists(self):
        path = "./"
        filename = "test_file__not_exists.tar.gz"
        timeout = 0.1
        is_created = watch.file(path, filename, timeout)
        self.assertFalse(is_created)

    def test_file__timeout(self):
        path = "./"
        filename = "test_file__timeout.tar.gz"
        wd = os.getcwd()
        w = WriteThread(os.path.join(wd, filename), 5, 0.1)
        w.start()
        timeout = 0.1
        is_created = watch.file(path, filename, timeout)
        w.stop()
        self.assertTrue(is_created)

    def test_file__other_file(self):
        log.set_level(log.Level.DEBUG)
        filename = "test_file__other_file.tar.gz"
        wd = os.getcwd()
        w = WriteThread(os.path.join(wd, "__" + filename), 5, 0.1)
        w.start()
        timeout = 1
        is_created = watch.file(wd, filename, timeout)
        w.stop()
        self.assertFalse(is_created)

    def test_file__already_exists(self):
        path = "./"
        filename = "test_file__already_exists.tar.gz"
        timeout = 0.1

        f = open(os.path.join(os.getcwd(), filename), "w")
        f.write("0")
        f.flush()
        f.close()

        is_created = watch.file(path, filename, timeout)
        self.assertTrue(is_created)
        os.remove(os.path.join(os.getcwd(), filename))
