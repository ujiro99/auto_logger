#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import time
from . import remote


class AutoLogger:

    time_fmt = "%Y-%m-%d_%H%M%S"
    log_name = "console.log"
    devnull = open('/dev/null', 'w')

    def __init__(self, address, test_number):
        """
         Constructor.
        :param str address: telnet address
        :param str test_number: test case number
        """
        self.host_name = address
        self.test_number = test_number
        self.local_log_dir = ""  # type: str

    def generate_date_str(self):
        """
        :rtype: str
        """
        t = time.localtime()
        return time.strftime(AutoLogger.time_fmt, t)

    def create_dir(self):
        """
        Create test case number + date directory.
        :rtype: str
        """
        path = os.path.join(os.getcwd(), self.test_number, self.generate_date_str())
        os.makedirs(path)
        if not os.path.exists(path):
            raise IOError
        return path

    def start(self):
        """
        Start logging.
        """
        self.local_log_dir = self.create_dir()
        path = os.path.join(self.local_log_dir, AutoLogger.log_name)
        subprocess.call(["script", path])
        return self.finish()

    def finish(self):
        """
        Copy logs to test case directory from remote.
        """
        params = remote.RemoteLoggerParam()
        params.host_name = self.host_name
        params.shell = ""
        params.log_cmd = ""
        params.remote_log_dir = ""
        params.remote_dist_dir = ""
        params.local_src_dir = ""
        params.local_dist_dir = self.local_log_dir

        remote_logger = remote.RemoteLogger(params)
        remote_logger.get_log()
        return remote_logger.move_log()
