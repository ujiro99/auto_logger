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
        extension = 'tar.gz'
        filename = wd + '/test.%s' % extension
        timeout = 10
        w = WriteThread(filename, 10, 0.1)
        w.start()
        f = watch.file(path, extension, timeout)
        w.stop()
        w.join()
        self.assertEqual(filename, f)

    def test_file__timeout(self):
        path = "./"
        extension = ".tar.gz"
        timeout = 0.1
        filename = watch.file(path, extension, timeout)
        self.assertIsNone(filename)
