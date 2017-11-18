#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import tempfile

import pandas as pd
from tqdm import tqdm

from logger import log


class ConvertParams:
    def __init__(self):
        self.log_path = None  # type: str
        self.script_path = None  # type: str
        self.file = None  # type: str


class Converter:
    DIR_SUFFIX = ".conv"  # type: str
    SED_ADD_FMT = "/%s/ s/$/%s/\n"  # type: str
    SED_CMD_FMT = "sed -r -f %s \"%s\" > \"%s\""  # type: str
    ESCAPE_CAR = ['\\', '/', '*', '.', '+', '?', '|', '{', '}', '(', ')', '[', ']', '^', '$']  # type: list of str
    SED_REPLACES = list(zip(ESCAPE_CAR, ['\\' + x for x in ESCAPE_CAR]))  # type: list of touple

    def __init__(self, params: ConvertParams):
        self.__p = params
        self.__tar_dir = None  # type: str

    def exec(self):
        """
        Execute conversion.
        """
        if not self.__is_files_exists():
            return False

        sc = self.__csv_to_sed_script()
        if self.__p.file is None:
            self.__un_tar()
            self.__exec_convert_tar(sc)
        else:
            self.__exec_convert(sc)
        os.unlink(sc)  # remote temp file

        return True

    def __is_files_exists(self):
        """
        Checks required files exists.
        :return: True: All file exists. False: Not exists.
        :rtype bool
        """
        if (not self.__p.log_path is None) and (not os.path.exists(self.__p.log_path)):
            log.w("- not found: %s" % self.__p.log_path)
            return False
        if (not self.__p.file is None) and (not os.path.exists(self.__p.file)):
            log.w("- not found: %s" % self.__p.file)
            return False
        if not os.path.exists(self.__p.script_path):
            log.w("- not found: %s" % self.__p.script_path)
            return False

        return True

    def __exec_convert(self, script_path):
        """
        Execute conversion using `sed` command.
        :param str script_path: Script file path, which is used by `sed` command.
        """
        # execute conversion
        f = os.path.splitext(self.__p.file)
        dp = f[0] + Converter.DIR_SUFFIX + f[1]
        log.i("- convert: %s" % dp)
        self.__call(Converter.SED_CMD_FMT % (script_path, self.__p.file, dp))

    def __exec_convert_tar(self, script_path):
        """
        Execute conversion a tar file.
        :param str script_path: Script file path, which will be used by `sed` command.
        """
        for d, f in tqdm(list(self.__files())):
            # create output directory.
            dist = os.path.join(self.__tar_dir + Converter.DIR_SUFFIX, d)
            if not os.path.exists(dist):
                os.makedirs(dist)

            # execute conversion
            sp = os.path.join(self.__tar_dir, d, f)
            dp = os.path.join(dist, f)
            log.d("- convert: %s" % dp)
            self.__call(Converter.SED_CMD_FMT % (script_path, sp, dp))

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
            d = root[len(self.__tar_dir) + 1:]
            for file in files:
                yield (d, file)

    def __csv_to_sed_script(self):
        """
        Generate sed script from csv file.
        :return: File path name.
        :rtype str
        """
        df = pd.read_csv(self.__p.script_path, names=('addr', 'cmd'))  # type: pandas.core.frame.DataFrame
        addr = df.addr.apply(lambda x: self.__escape_sed_addr(x))

        with tempfile.NamedTemporaryFile(mode='w+t', delete=False) as tf:
            for i, r in df.iterrows():
                tf.write(Converter.SED_ADD_FMT % (addr[i], r[1]))
        return tf.name

        # remain script file for debug.
        # f = "tests/test.sed"
        # with open(f, "w") as fd:
        #     for i, r in df.iterrows():
        #         fd.write(Converter.SED_ADD_FMT % (addr[i], r[1]))
        # return f

    def __escape_sed_addr(self, address):
        """
        Escape sed address string.
        :param str address: Address string which is escaped.
        :return: Escaped string.
        :rtype str
        """
        for c, r in Converter.SED_REPLACES:
            address = address.replace(c, r)
        return address
