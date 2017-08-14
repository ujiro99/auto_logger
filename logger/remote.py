#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import shutil
import time

import pexpect

from . import watch, log


class RemoteLogger:
    PROMPT = "[#$%>]"
    TIMEOUT_EXPECT = 20
    TIMEOUT_LOGGING = 30
    TIMEOUT_MOVE = 30
    TMP_FILE = "__tmp__"

    def __init__(self, params):
        """
        constructor
        :param logger.params.LogParam params: execution parameter
        """
        self.params = params  # type: import logger.params
        self.filename = None  # type: str
        self.p = None  # type: pexpect.spawn

    def get_log(self):
        """
        Get remote log using shell command.
        :return Result of logging. success: True, failed: False
        :rtype bool
        """
        # launch shell
        log.i("- launch %s@%s" % (self.params.shell, self.params.host_name))
        self.p = p = pexpect.spawn("%s %s" % (self.params.shell, self.params.host_name))
        # self.p = p = pexpect.spawn("bash") # for develop

        log.d("- check is required to add known hosts.")
        p.expect([r"yes", r"[#$%>]"])
        log.d(p.before)
        log.d(p.after)
        if p.after == b'yes':
            log.d("-- required.")
            self.__send('yes')

        log.d("- prepare logging")
        p.timeout = RemoteLogger.TIMEOUT_EXPECT
        self.__send("PS1='#'")
        self.__send("cd %s" % self.params.remote_log_dir)
        self.__send("touch %s.%s" % (RemoteLogger.TMP_FILE, self.params.log_extension))

        # check current files.
        before = self.__get_file_set()
        log.d(before)

        # execute log command
        # self.params.log_cmd = "touch 1." + self.params.log_extension  # for develop
        self.__send(self.params.log_cmd)
        log.i("- execute %s" % self.params.log_cmd)

        # wait log file created
        timeout = RemoteLogger.TIMEOUT_LOGGING
        while timeout > 0:
            time.sleep(1)
            timeout -= 1
            after = self.__get_file_set()
            created = after - before
            if len(created) != 0:
                break

        self.__send("rm %s.%s" % (RemoteLogger.TMP_FILE, self.params.log_extension))
        if timeout <= 0:
            log.w("- time out to logging.")
            return False  # Failed to logging
        self.filename = created.pop()
        log.i("- created: " + self.filename)

        # mv log file to local machine
        log.i("- move file to %s" % self.params.remote_dist_dir)
        self.__send("mv %s %s" % (self.filename, self.params.remote_dist_dir))

        # terminate
        p.terminate()
        p.expect(pexpect.EOF)

        return True

    def __send(self, cmd):
        """
        Send command to shell.
        :param str cmd: Command string to be send.
        """
        if cmd is None:
            log.w("Error: cmd is None")
            return

        log.d("  > " + cmd)
        self.p.sendline(cmd)
        self.p.expect(RemoteLogger.PROMPT)
        log.d(self.p.before)

    def __get_file_set(self):
        """
        Get current directory's file set.
        :return: File set.
        :rtype set
        """
        self.p.sendline("ls *.%s -1 --color=no" % self.params.log_extension)
        self.p.expect("no(.*)" + RemoteLogger.PROMPT)
        ls = self.p.match.groups()[0].decode("utf-8")  # type: str
        f = lambda x: bool(re.match('\S+', x))
        ret = set(filter(f, ls.splitlines()))
        log.d(ret)
        return ret

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
            log.w("- not found: %s" % log_path)
            return False

        shutil.move(log_path, self.params.local_dist_dir)
        log.i("- moved: %s" % self.params.local_dist_dir)

        return True
