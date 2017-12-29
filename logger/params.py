#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import os
import os.path as path


class LogParam:
    FILE_NAME = 'plog.ini'
    DEFAULT = 'DEFAULT'

    def __init__(self):
        self.host_name = None  # type: str
        self.shell = None  # type: str
        self.log_cmd = None  # type: str
        self.log_extension = None  # type: str
        self.remote_log_dir = None  # type: str
        self.remote_dist_dir = None  # type: str
        self.local_src_dir = None  # type: str
        self.local_dist_dir = None  # type: str
        self.convert_rule = None  # type: str
        self.merge_dir = None  # type: str
        self.usb_dir = None  # type: str

    def read_ini(self):
        """
        Read settings from ini file.
        :return: Result of reading. True: success | False: fail
        :rtype: bool
        """

        # read from ini file
        ini_file = configparser.ConfigParser()
        if path.exists(path.join(os.getcwd(), LogParam.FILE_NAME)):
            ini_file.read(path.join(os.getcwd(), LogParam.FILE_NAME))
        elif path.exists(path.join(os.environ['HOME'], LogParam.FILE_NAME)):
            ini_file.read(path.join(os.environ['HOME'], LogParam.FILE_NAME))
        else:
            return False

        # set params to member
        f = ini_file[LogParam.DEFAULT]
        self.host_name = f['host_name']
        self.shell = f['shell']
        self.log_cmd = f['log_cmd']
        self.log_extension = f['log_extension']
        self.remote_log_dir = f['remote_log_dir']
        self.remote_dist_dir = f['remote_dist_dir']
        self.local_src_dir = f['local_src_dir']
        self.convert_rule = f['convert_rule']
        self.merge_dir = f['merge_dir']
        self.usb_dir = f['usb_dir']

        return True

    def write_ini(self):
        """
        Write settings to ini file.
        :return: file path which settings written.
        :rtype: str
        """

        # set member to params
        ini_file = configparser.ConfigParser()
        ini_file[LogParam.DEFAULT] = {
            'host_name':       self.host_name,
            'shell':           self.shell,
            'log_cmd':         self.log_cmd,
            'log_extension':   self.log_extension,
            'remote_log_dir':  self.remote_log_dir,
            'remote_dist_dir': self.remote_dist_dir,
            'local_src_dir':   self.local_src_dir,
            'convert_rule':    self.convert_rule,
            'merge_dir':       self.merge_dir,
            'usb_dir':         self.usb_dir
        }

        # write to ini file
        file_path = path.join(os.environ['HOME'], LogParam.FILE_NAME)
        with open(file_path, 'w') as file:
            ini_file.write(file)

        return file_path
