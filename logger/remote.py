#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
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
        self.__connect()

        log.d("- prepare logging")

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
            time.sleep(0.1)
            timeout -= 0.1
            after = self.__get_file_set()
            created = after - before
            if len(created) != 0:
                break

        if timeout <= 0:
            log.w("- time out to logging.")
            return False  # Failed to logging
        self.filename = created.pop()
        log.i("- created: " + self.filename)

        # mv log file to local machine
        log.i("- move file to %s" % self.params.remote_dist_dir)
        self.__send("mv %s %s" % (self.filename, self.params.remote_dist_dir))

        self.__disconnect()
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
            log.w("- not found: %s" % log_path)
            return False

        shutil.move(log_path, self.params.local_dist_dir)
        log.i("- moved: %s" % self.params.local_dist_dir)

        return True

    def list_log(self):
        """
        List remote log files.
        :return: List of files
        :rtype list of str
        """
        self.__connect()
        ls = self.__get_file_list()
        self.__disconnect()
        return ls

    def __connect(self):
        """
        Connect to remote shell.
        """
        # launch shell
        log.i("- launch %s to %s" % (self.params.shell, self.params.host_name))
        self.p = p = pexpect.spawn("%s %s" % (self.params.shell, self.params.host_name))
        # self.p = p = pexpect.spawn("bash") # for develop

        log.d("- check is required to add known hosts.")
        p.expect([r"yes", r"[#$%>]"])
        log.d(p.before)
        log.d(p.after)
        if p.after == b'yes':
            log.d("-- required.")
            self.__send('yes')
        p.timeout = RemoteLogger.TIMEOUT_EXPECT
        self.__send("PS1='#'")
        self.__send("cd %s" % self.params.remote_log_dir)

    def __disconnect(self):
        """
        Disconnect from remote shell.
        """
        self.p.terminate()
        self.p.expect(pexpect.EOF)

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
        :rtype set of str
        """
        return set(self.__get_file_list())

    def __get_file_list(self):
        """
        Get current directory's file list
        :return: File list.
        :rtype list of str
        """
        tmp_file = "%s.%s" % (RemoteLogger.TMP_FILE, self.params.log_extension)

        self.__send("touch " + tmp_file)
        self.p.sendline("ls *.%s -1 --color=no" % self.params.log_extension)
        self.p.expect("no(.*)" + RemoteLogger.PROMPT)

        ls = self.p.match.groups()[0].decode("utf-8")  # type: str
        ls = list(filter(lambda x: bool(re.match('\S+', x)), ls.splitlines()))
        ls.remove(tmp_file)

        self.__send("rm " + tmp_file)
        log.d(ls)
        return ls
