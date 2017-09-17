#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
from unittest import TestCase
from unittest.mock import MagicMock, patch

import pexpect

import logger.auto
import logger.params
from logger import remote, watch


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

        self.assertTrue(ret)
        is_exists = os.path.exists(os.path.join(p.local_dist_dir, l.filename))
        self.assertTrue(is_exists)
        shutil.rmtree(p.local_dist_dir)

    @patch.object(pexpect, 'spawn', MagicMock(return_value=MagicMock))
    def test_get_log_timeout(self):
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
        self.assertFalse(ret)

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
        self.assertTrue(ret)

        is_exists = os.path.exists(os.path.join(p.local_dist_dir, filename))
        self.assertTrue(is_exists)
        shutil.rmtree(p.local_dist_dir)

    @patch.object(watch, 'file', MagicMock(return_value=True))
    def test_move_log_glob(self):
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
        self.assertTrue(ret)
        self.assertTrue(os.path.exists(os.path.join(p.local_dist_dir, filename + '1')))
        self.assertTrue(os.path.exists(os.path.join(p.local_dist_dir, filename + '2')))
        shutil.rmtree(p.local_dist_dir)

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

        self.assertFalse(ret)

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

        self.assertFalse(ret)

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
