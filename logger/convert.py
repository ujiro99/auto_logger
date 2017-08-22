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
        self.__un_tar()
        con_dir = self.__tar_dir + Converter.DIR_SUFFIX
        if not os.path.exists(con_dir):
            os.makedirs(con_dir)
        for d, f in self.__files(self.__tar_dir):
            log.i("convert: " + f)
            self.__call("cat %s/%s | sed -f %s > %s/%s" % (d, f, self.__p.script_path, con_dir, f))

    def __un_tar(self):
        self.__tar_dir = os.path.splitext(os.path.splitext(self.__p.log_path)[0])[0]
        if not os.path.exists(self.__tar_dir):
            os.makedirs(self.__tar_dir)
        self.__call("tar xf %s -C %s" % (self.__p.log_path, self.__tar_dir))

    def __call(self, cmd):
        log.d(cmd)
        return subprocess.call(cmd, shell=True)

    def __files(self, dir_name):
        for root, dirs, files in os.walk(dir_name):
            for file in files:
                yield (root, file)
