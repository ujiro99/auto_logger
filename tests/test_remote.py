#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from unittest import TestCase
from unittest.mock import MagicMock, patch

import pexpect

import logger.auto
import logger.params
from logger import remote, watch


MNT_USB = "/tmp"

class TestRemoteLogger(TestCase):
    def test_get_log(self):
        p = logger.params.LogParam()
        p.host_name = 'root@172.30.10.2'
        p.shell = 'ssh'
        p.log_cmd = 'log_to_rom'
        p.log_extension = 'tar.gz'
        p.remote_log_dir = '/root'
        p.remote_dist_dir = '/mnt/log'
        p.local_src_dir = '.'
        p.local_dist_dir = os.path.join(os.getcwd(), "dist")
        if not os.path.exists(p.local_dist_dir):
            os.mkdir(p.local_dist_dir)

        l = remote.RemoteLogger(p)
        ret = l.get_log()

        self.assertTrue(os.path.exists(ret[0]))
        os.remove(ret[0])

    @patch.object(pexpect, 'spawn', MagicMock(return_value=MagicMock))
    def test_get_log__timeout(self):
        params = logger.params.LogParam()
        params.log_extension = "tar.gz"
        remote_logger = remote.RemoteLogger(params)
        remote.RemoteLogger.TIMEOUT_LOGGING = 0.5

        p = pexpect.spawn()
        p.expect = MagicMock()
        p.sendline = MagicMock()
        p.match = MagicMock()
        p.terminate = MagicMock()
        p.before = None
        p.after = None
        array = [MagicMock()]
        p.match.groups = MagicMock(return_value=array)
        sentinel = "__tmp__.%s" % params.log_extension
        array[0].decode = MagicMock(return_value=sentinel)

        ret = remote_logger.get_log()
        self.assertEqual(ret, None)

    def test_get_log__usb(self):
        p = logger.params.LogParam()
        p.host_name = 'root@172.30.10.2'
        p.shell = 'ssh'
        p.log_cmd = 'log_to_rom'
        p.log_extension = 'tar.gz'
        p.remote_log_dir = '/root'

        ret = remote.RemoteLogger(p).get_log(to_usb=True)

        df = os.path.join(MNT_USB, os.path.basename(ret[0]))
        self.assertTrue(os.path.exists(df))

    @patch.object(watch, 'file', MagicMock(return_value=True))
    def test_move_log(self):
        os.chdir("tests")
        p = logger.params.LogParam()
        p.read_ini()
        os.chdir("..")
        p.remote_log_dir = "/mnt/log"
        p.local_src_dir = os.getcwd()
        p.local_dist_dir = os.path.join(os.getcwd(), "dist")

        # create src file, and dist directory
        filename = "testdata"
        f = open(os.path.join(os.getcwd(), filename), "w")
        f.close()
        if not os.path.exists(p.local_dist_dir):
            os.mkdir(p.local_dist_dir)

        # exec
        ret = remote.RemoteLogger(p).move_log(filename)

        for f in ret:
            self.assertTrue(os.path.exists(f))
            os.remove(f)

    @patch.object(watch, 'file', MagicMock(return_value=True))
    def test_move_log__glob(self):
        os.chdir("tests")
        p = logger.params.LogParam()
        p.read_ini()
        os.chdir("..")
        p.remote_log_dir = "/mnt/log"
        p.local_src_dir = os.getcwd()
        p.local_dist_dir = os.path.join(os.getcwd(), "dist")

        # create src file, and dist directory
        filename = "testdata"
        f = open(os.path.join(os.getcwd(), filename + '1'), "w")
        f.close()
        f = open(os.path.join(os.getcwd(), filename + '2'), "w")
        f.close()
        if not os.path.exists(p.local_dist_dir):
            os.mkdir(p.local_dist_dir)

        # exec
        ret = remote.RemoteLogger(p).move_log(filename + '*')
        self.assertTrue(len(ret) == 2)
        self.assertTrue(ret[0])
        self.assertTrue(ret[1])
        os.remove(ret[0])
        os.remove(ret[1])

    def test_move_log__usb(self):
        os.chdir("tests")
        p = logger.params.LogParam()
        p.read_ini()
        os.chdir("..")
        p.remote_log_dir = "/mnt/log"

        # exec
        filename = "testfile_test_move_log__usb"
        fd = open(filename, "w")
        fd.close()
        remote.RemoteLogger(p).move_log(filename, to_usb=True)

        df = os.path.join(MNT_USB, filename)
        self.assertTrue(os.path.exists(df))

    def test_move_log__not_found(self):
        os.chdir("tests")
        p = logger.params.LogParam()
        p.read_ini()
        os.chdir("..")
        p.remote_log_dir = "/mnt/log"
        p.local_src_dir = os.getcwd()
        p.local_dist_dir = os.path.join(os.getcwd(), "dist")
        remote.RemoteLogger.TIMEOUT_MOVE = 1

        filename = "testdata"
        r = remote.RemoteLogger(p)
        ret = r.move_log(filename)

        self.assertEqual(ret, None)

    @patch.object(watch, 'file', MagicMock(return_value=False))
    def test_move_log__move_failed(self):
        p = logger.params.LogParam()
        p.read_ini()

        r = remote.RemoteLogger(p)
        r._RemoteLogger__connect = MagicMock()
        r._RemoteLogger__disconnect = MagicMock()
        r._RemoteLogger__get_file_list = MagicMock(return_value=[None, 'test'])
        r._RemoteLogger__send = MagicMock()

        filename = "testdata"
        ret = r.move_log(filename)

        self.assertEqual(ret, None)

    def test_list_log(self):
        files = ["1.tar.gz", "2.tar.gz"]
        for f in files:
            with open(f, "w") as fd:
                fd.write("")

        os.chdir("./tests")
        p = logger.params.LogParam()
        p.read_ini()
        p.remote_log_dir = "/mnt/log"
        remote_logger = remote.RemoteLogger(p)
        ls = remote_logger.list_log()
        self.assertEqual(ls, files)

        os.chdir("..")
        for f in files:
            os.remove(f)

    def test_clear_log(self):
        files = ["3.tar.gz", "4.tar.gz"]
        for f in files:
            with open(f, "w") as fd:
                fd.write("")

        os.chdir("./tests")
        p = logger.params.LogParam()
        p.read_ini()
        p.remote_log_dir = "/mnt/log"

        remote.RemoteLogger(p).clear_log()

        os.chdir("..")
        for f in files:
            self.assertFalse(os.path.exists(f))
