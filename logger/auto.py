#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pexpect
import time
from . import remote


class AutoLogger:

    TIME_FMT = "%Y-%m-%d_%H%M%S"
    CONSOLE_LOG_NAME = "console.log"
    END_LINE = "\r\n"
    PROMPT = "[#$%>]"
    SHELL = "ssh"
    TIMEOUT_EXPECT = 10

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
        return time.strftime(AutoLogger.TIME_FMT, t)

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
        path = os.path.join(self.local_log_dir, AutoLogger.CONSOLE_LOG_NAME)

        # 操作記録のため、script コマンドを開始
        p = pexpect.spawn("%s %s" % ("script", path))
        p.timeout = AutoLogger.TIMEOUT_EXPECT

        # ユーザ操作前に自動実行したい処理があればここにいれる
        # ex)
        #   p.expect(AutoLogger.PROMPT)             # 入力待ちを検知する
        #   p.send("%s\n" % "${実行したいコマンド}")   # コマンドを実行する

        # shell に接続
        p.expect(AutoLogger.END_LINE)
        p.send("%s %s\n" % (AutoLogger.SHELL, self.host_name))

        # ユーザ操作開始
        p.interact()
        # 終了
        p.terminate()
        p.expect(pexpect.EOF)
        return True

    def finish(self):
        """
        Copy logs to test case directory from remote.
        """
        params = remote.RemoteLoggerParam()
        params.host_name = self.host_name
        params.shell = AutoLogger.SHELL
        params.log_cmd = ""
        params.remote_log_dir = ""
        params.remote_dist_dir = ""
        params.local_src_dir = ""
        params.local_dist_dir = self.local_log_dir

        remote_logger = remote.RemoteLogger(params)
        remote_logger.get_log()
        return remote_logger.move_log()
