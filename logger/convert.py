#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess

from logger import log


class ConvertParams:
    def __init__(self):
        self.log_path = None  # type: str
        self.script_path = None  # type: str


class Converter:
    DIR_SUFFIX = ".conv"

    def __init__(self, params: ConvertParams):
        self.__p = params
        self.__tar_dir = None  # type: str

    def exec(self):
        """
        Execute conversion using `sed` command.
        """
        self.__un_tar()
        for d, f in self.__files(self.__tar_dir):

            # create output directory.
            dist = os.path.join(self.__tar_dir + Converter.DIR_SUFFIX, d)
            if not os.path.exists(dist):
                os.makedirs(dist)

            # execute conversion
            src_path = os.path.join(self.__tar_dir, d, f)
            dist_path = os.path.join(dist, f)
            log.i("convert: %s" % dist_path)
            self.__call("cat %s | sed -f %s > %s" % (src_path, self.__p.script_path, dist_path))

    def __un_tar(self):
        """
        Extract a __p.log_path tar file.
        """
        self.__tar_dir = os.path.splitext(self.__p.log_path)[0]
        if not os.path.exists(self.__tar_dir):
            os.makedirs(self.__tar_dir)
        self.__call("tar xf %s -C %s" % (self.__p.log_path, self.__tar_dir))

    def __call(self, cmd):
        """
        Execute a command.
        :param str cmd: Command string.
        :return: Return code of the command.
        :rtype int
        """
        log.d(cmd)
        return subprocess.call(cmd, shell=True)

    def __files(self, dir_name):
        """
        Find files.
        :param str dir_name: Target directory name.
        :return: Iterator[str]
        """
        for root, dirs, files in os.walk(dir_name):
            d = root.lstrip(dir_name).lstrip('/')
            for file in files:
                yield (d, file)
