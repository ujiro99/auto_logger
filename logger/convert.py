#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import tempfile

import pandas as pd

from logger import log


class ConvertParams:
    def __init__(self):
        self.log_path = None  # type: str
        self.script_path = None  # type: str


class Converter:
    DIR_SUFFIX = ".conv"
    SED_ADD_FMT = "/%s/ s/$/%s/\n"

    def __init__(self, params: ConvertParams):
        self.__p = params
        self.__tar_dir = None  # type: str

    def exec(self):
        """
        Execute conversion.
        """
        if not self.__is_files_exists():
            return False

        self.__un_tar()
        sc = self.__csv_to_sed_script()
        self.__exec_convert(sc)
        os.unlink(sc)  # remote temp file

        return True

    def __is_files_exists(self):
        """
        Checks required files exists.
        :return: True: All file exists. False: Not exists.
        :rtype bool
        """
        if not os.path.exists(self.__p.log_path):
            log.w("- not found: %s" % self.__p.log_path)
            return False
        if not os.path.exists(self.__p.script_path):
            log.w("- not found: %s" % self.__p.script_path)
            return False
        return True

    def __exec_convert(self, script_path):
        """
        Execute conversion using `sed` command.
        :param str script_path: Script file path, which will be used by `sed` command.
        """
        for d, f in self.__files():
            # create output directory.
            dist = os.path.join(self.__tar_dir + Converter.DIR_SUFFIX, d)
            if not os.path.exists(dist):
                os.makedirs(dist)

            # execute conversion
            src_path = os.path.join(self.__tar_dir, d, f)
            dist_path = os.path.join(dist, f)
            log.i("- convert: %s" % dist_path)
            self.__call("cat %s | sed -r -f %s > %s" % (src_path, script_path, dist_path))

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
        log.d(" > %s" % cmd)
        return subprocess.call(cmd, shell=True)

    def __files(self):
        """
        Find files.
        :return: Iterator[str]
        """
        for root, dirs, files in os.walk(self.__tar_dir):
            d = root.lstrip(self.__tar_dir).lstrip('/')
            for file in files:
                yield (d, file)

    def __csv_to_sed_script(self):
        """
        Generate sed script from csv file.
        :return: File path name.
        :rtype str
        """
        df = pd.read_csv(self.__p.script_path, names=('addr', 'cmd'))  # type: pandas.core.frame.DataFrame
        addr = df.addr.apply(lambda x: re.escape(x))
        with tempfile.NamedTemporaryFile(mode='w+t', delete=False) as tf:
            for i, r in df.iterrows():
                tf.write(Converter.SED_ADD_FMT % (addr[i], r[1]))
        return tf.name
