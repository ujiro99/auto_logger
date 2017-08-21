#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import re

import pexpect

from logger import remote


class AutoLogger:
    TIME_FMT = "%Y-%m-%d_%H%M%S"
    CONSOLE_LOG_NAME = "console.log"
    END_LINE = "\r\n"
    PROMPT = "[#$%>]"
    TIMEOUT_EXPECT = 10

    def __init__(self, params, test_number=None):
        """
         Constructor.
        :param logger.params.LogParam params: Parameters to decide behaviors of command.
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

    def generate_serial_number(self):
        """
        :rtype: str
        """
        path = os.path.join(os.getcwd(), self.test_number)
        if not os.path.exists(path):
            return '01'

        items = os.listdir(path)
        dirs = [x for x in items if not re.match('^\d*$', x) is None]
        if len(dirs) == 0:
            return '01'
        else:
            return '{0:02d}'.format(int(max(dirs)) + 1)

    def create_dir(self):
        """
        Create test case number + date directory.
        :rtype: str
        """
        path = os.path.join(os.getcwd(), self.test_number, self.generate_serial_number())
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
        #   p.sendline("%s" % "${実行したいコマンド}")   # コマンドを実行する

        # shell に接続
        p.expect(AutoLogger.END_LINE)
        p.sendline("%s %s" % (self.params.shell, self.params.host_name))

        # ここからユーザ操作開始
        p.interact()
        # 終了
        p.terminate()
        p.expect(pexpect.EOF)
        return True

    def start(self):
        """
        Executes all logging process.
        :return: Result of getting remote log. True: success | False: fail
        :rtype: bool
        """
        # create log directory
        self.params.local_dist_dir = self.create_dir()

        # get console log
        self.start_script_cmd()

        # get remote log
        remote_logger = remote.RemoteLogger(self.params)
        remote_logger.get_log()
        return remote_logger.move_log()

    def get(self):
        """
        Get a remote log.
        :return: Result of getting remote log. True: success | False: fail
        :rtype: bool
        """
        self.params.local_dist_dir = os.getcwd()
        remote_logger = remote.RemoteLogger(self.params)
        remote_logger.get_log()
        return remote_logger.move_log()
