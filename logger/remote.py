#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import time
import pexpect


class RemoteLogger:

    PROMPT = "[#$%>]"
    TIMEOUT_EXPECT = 10
    TIMEOUT_MOVE = 30

    def __init__(self, params):
        """
        constructor
        :param logger.params.LogParam params: execution parameter
        """
        self.params = params  # type: import logger.params
        self.filename = None  # type: str

    def get_log(self):
        """
        Get remote log using shell command.
        """
        # launch shell
        print("- launch %s@%s" % (self.params.shell, self.params.host_name))
        p = pexpect.spawn("%s %s" % (self.params.shell, self.params.host_name))
        p.timeout = RemoteLogger.TIMEOUT_EXPECT

        # execute log command
        p.expect(RemoteLogger.PROMPT)
        p.send("%s\n" % self.params.log_cmd)
        print("- execute %s" % self.params.log_cmd)

        # move to log directory
        p.expect(RemoteLogger.PROMPT)
        p.send("cd %s\n" % self.params.remote_log_dir)

        # get log file name
        p.expect(RemoteLogger.PROMPT)
        p.send("ls -t | head -1\n")
        p.expect("-1\s+(\S+)\s")
        self.filename = p.match.groups()[0].decode("utf-8")
        print("- created: %s" % self.filename)

        # mv log file to local machine
        print("- move log file")
        p.expect(RemoteLogger.PROMPT)
        p.send("mv %s %s\n" % (self.filename, self.params.remote_dist_dir))

        # terminate
        p.expect(RemoteLogger.PROMPT)
        p.terminate()
        p.expect(pexpect.EOF)

    def move_log(self):
        """
        Moves remote log to local directory.
        :return: Result of logging. True: success | False: fail
        :rtype: bool
        """
        log_path = os.path.join(self.params.local_src_dir, self.filename)

        # check is file exists
        timeout = RemoteLogger.TIMEOUT_MOVE
        while (not os.path.exists(log_path)) and timeout > 0:
            time.sleep(1)
            timeout -= 1

        if timeout <= 0:
            # file not exists.
            print("- timeout")
            return False

        shutil.move(log_path, self.params.local_dist_dir)
        return True
