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

    def __init__(self, params):
        """
        constructor
        :param logger.params.LogParam params: execution parameter
        """
        self.params = params  # type: import logger.params
        self.p = None  # type: pexpect.spawn

    def get_log(self, to_usb=False):
        """
        Get remote log using shell command.
        :param bool to_usb: If true, log file is copied to USB.
        :return: Log file name. If failed, returns None.
        :rtype: list of str
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
            self.__disconnect()
            return None  # Failed to logging

        f = created.pop()
        log.i("- created: " + f)

        ls = self.__move_file([f], to_usb)
        self.__disconnect()
        return ls

    def move_log(self, file_name, to_usb=False):
        """
        Move specified file from remote_log_dir to remote_dist_dir .
        :param str file_name: File name to be moved.
        :param bool to_usb: If true, log file is copied to USB.
        :return: Log file name. If failed, returns None.
        :rtype: list of str
        """
        self.__connect()

        ls, err = self.__get_file_list(file_name)
        if (not err is None) or (len(ls) <= 0):
            log.w("- not found: %s" % file_name)
            ls = None
        else:
            ls = self.__move_file(ls, to_usb)

        self.__disconnect()
        return ls

    def list_log(self):
        """
        List remote log files in remote_log_dir.
        :return: List of files
        :rtype list of str
        """
        self.__connect()
        ls, err = self.__get_file_list()
        if not err is None: log.w(err)
        self.__disconnect()
        return ls

    def clear_log(self):
        """
        Remove all remote log files in remote_log_dir.
        """
        self.__connect()
        self.__send("rm *.%s" % self.params.log_extension)
        time.sleep(0.1)
        self.__disconnect()

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
        return set(self.__get_file_list()[0])

    def __get_file_list(self, pattern=None):
        """
        Get current directory's file list
        :return: File list and error message(if error occurred).
        :rtype (list of str, str)
        """
        if pattern is None: pattern = '*.' + self.params.log_extension

        self.p.sendline("ls %s -1 --color=no" % pattern)
        self.p.expect("no(.*)" + RemoteLogger.PROMPT)

        ls = self.p.match.groups()[0].decode("utf-8")  # type: str
        if ls.find("No such file or directory") > 0:
            return [], "File not found."

        ls = list(filter(lambda x: bool(re.match('\S+', x)), ls.splitlines()))
        log.d(ls)
        return ls, None

    def __move_file(self, files, to_usb=False):
        """
        Move files.
        :param list of str files: target file names
        :param bool to_usb: if true, move files to usb.
        :return Moved file list.
        :rtype list of str
        """
        if to_usb:
            return self.__move_file_to_usb(files)
        else:
            return self.__move_file_to_shared_dir(files)

    def __move_file_to_usb(self, files):
        """
        Move files to remote_dist_dir -> usb.
        :param list of str files: target file names
        :return Moved file list.
        :rtype list of str
        """
        usb_dir = "/mnt/USB0"

        # mv log file to usb
        ls = []
        log.i("- move file to %s" % usb_dir)
        for f in files:
            self.__send("mv %s %s" % (f, usb_dir))
            self.__send("sync")
            ls.append(os.path.join(usb_dir, f))

        return ls

    def __move_file_to_shared_dir(self, files):
        """
        Move files to remote_dist_dir -> local_dist_dir.
        :param list of str files: target file names
        :return Moved file list.
        :rtype list of str
        """
        ret = []
        for f in files:
            # mv log file - remote to local
            log.i("- move file to %s" % self.params.remote_dist_dir)
            self.__send("mv %s %s" % (f, self.params.remote_dist_dir))
            is_created = watch.file(self.params.local_src_dir, f, RemoteLogger.TIMEOUT_MOVE)

            if not is_created:
                log.w("- move failed: %s" % f)
                continue

            # mv log file - local to local
            sp = os.path.join(self.params.local_src_dir, f)
            dp = os.path.join(self.params.local_dist_dir, f)
            shutil.move(sp, self.params.local_dist_dir)
            ret.append(dp)
            log.i("- moved: %s" % dp)

        return ret
