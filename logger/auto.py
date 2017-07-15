#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pexpect
import time
from . import remote


class LogParam:

    def __init__(self):
        self.host_name = None        # type: str
        self.shell = None            # type: str
        self.log_cmd = None          # type: str
        self.remote_log_dir = None   # type: str
        self.remote_dist_dir = None  # type: str
        self.local_src_dir = None    # type: str
        self.local_dist_dir = None   # type: str


class AutoLogger:

    TIME_FMT = "%Y-%m-%d_%H%M%S"
    CONSOLE_LOG_NAME = "console.log"
    END_LINE = "\r\n"
    PROMPT = "[#$%>]"
    TIMEOUT_EXPECT = 10

    def __init__(self, params, test_number):
        """
         Constructor.
        :param LogParam params: Parameters to decide behaviors of command.
        :param str test_number: Test case number.
        """
        self.params = params
        self.test_number = test_number

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

    def start_script_cmd(self):
        """
        Start logging.
        """
        path = os.path.join(self.params.local_dist_dir, AutoLogger.CONSOLE_LOG_NAME)

        # 操作記録のため、script コマンドを開始
        p = pexpect.spawn("%s %s" % ("script", path))
        p.timeout = AutoLogger.TIMEOUT_EXPECT

        # ユーザ操作前に自動実行したい処理があればここにいれる
        # ex)
        #   p.expect(AutoLogger.PROMPT)             # 入力待ちを検知する
        #   p.send("%s\n" % "${実行したいコマンド}")   # コマンドを実行する

        # shell に接続
        p.expect(AutoLogger.END_LINE)
        p.send("%s %s\n" % (self.params.shell, self.params.host_name))

        # ユーザ操作開始
        p.interact()
        # 終了
        p.terminate()
        p.expect(pexpect.EOF)
        return True

    def execute(self):
        # create log directory
        self.params.local_dist_dir = self.create_dir()

        # get console log
        self.start_script_cmd()

        # get remote log
        remote_logger = remote.RemoteLogger(self.params)
        remote_logger.get_log()
        return remote_logger.move_log()

