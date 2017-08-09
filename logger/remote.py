#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import shutil
import pexpect

from . import watch


class RemoteLogger:

    PROMPT = "[#$%>]"
    TIMEOUT_EXPECT = 20
    TIMEOUT_LOGGING = 30
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
        :return Result of logging. success: True, failed: False
        :rtype bool
        """
        # launch shell
        print("- launch %s@%s" % (self.params.shell, self.params.host_name))
        p = pexpect.spawn("%s %s" % (self.params.shell, self.params.host_name))
        p.timeout = RemoteLogger.TIMEOUT_EXPECT

        # move to log directory
        p.expect(RemoteLogger.PROMPT)
        p.sendline("cd %s" % self.params.remote_log_dir)

        # create sentinel file
        sentinel = "__tmp__.%s" % self.params.log_extension
        p.expect(RemoteLogger.PROMPT)
        p.sendline("%s %s" % ("touch", sentinel))

        # execute log command
        p.expect(RemoteLogger.PROMPT)
        p.sendline("%s" % self.params.log_cmd)
        print("- execute %s" % self.params.log_cmd)

        # wait log to be created, and get log file name
        n = sentinel
        timeout = RemoteLogger.TIMEOUT_LOGGING
        while (n == sentinel) and (timeout > 0):
            time.sleep(1)
            timeout -= 1
            p.expect(RemoteLogger.PROMPT)
            p.sendline("ls -t *.%s | head -1" % self.params.log_extension)
            p.expect("-1\s+(\S+)\s")
            n = p.match.groups()[0].decode("utf-8")

        if timeout <= 0:
            print("- time out to logging.")
            return False # Failed to logging

        p.sendline("rm %s" % sentinel)
        self.filename = n
        print("- created: %s" % self.filename)

        # mv log file to local machine
        print("- move log file: %s" % self.params.remote_dist_dir)
        p.expect(RemoteLogger.PROMPT)
        p.sendline("mv %s %s" % (self.filename, self.params.remote_dist_dir))

        # terminate
        p.expect(RemoteLogger.PROMPT)
        p.terminate()
        p.expect(pexpect.EOF)

        return True


    def move_log(self):
        """
        Move log file
        :return Result fo move. success: True, failed: False.
        :rtype bool
        """
        is_created = watch.file(self.params.local_src_dir,
                                self.filename,
                                RemoteLogger.TIMEOUT_MOVE)

        log_path = os.path.join(self.params.local_src_dir, self.filename)
        if not is_created:
            print("- not found: %s" % log_path)
            return False

        shutil.move(log_path, self.params.local_dist_dir)
        print("- moved: %s" % self.params.local_dist_dir)

        return True
