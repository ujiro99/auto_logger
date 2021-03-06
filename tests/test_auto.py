#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
from unittest import TestCase
from unittest.mock import MagicMock, patch

import pexpect

import logger.params
from logger import auto, remote, convert


class TestAutoLogger(TestCase):
    test_number = "1-1-1"
    p = logger.params.LogParam()
    p.host_name = "192.168.1.2"
    p.shell = "ssh"
    p.log_cmd = ""
    p.remote_log_dir = ""
    p.remote_dist_dir = ""
    p.local_src_dir = ""
    p.local_dist_dir = ""
    p.convert_rule = "./tests/rule.csv"

    def test_generate_date_str(self):
        a = auto.AutoLogger(TestAutoLogger.p, TestAutoLogger.test_number)
        date_str = a.generate_date_str()
        self.assertRegex(date_str, "\d\d-\d\d-\d\d_\d\d\d\d\d\d")

    def test_generate_serial_number(self):
        a = auto.AutoLogger(TestAutoLogger.p, TestAutoLogger.test_number)
        os.makedirs(os.path.join(os.getcwd(), TestAutoLogger.test_number))
        dir_name = a.generate_serial_number()
        self.assertEqual(dir_name, "01")
        shutil.rmtree(os.path.join(os.getcwd(), TestAutoLogger.test_number))

    def test_generate_serial_number__dir_not_exists(self):
        a = auto.AutoLogger(TestAutoLogger.p, TestAutoLogger.test_number)
        dir_name = a.generate_serial_number()
        self.assertEqual(dir_name, "01")

    def test_generate_serial_number__01_10a(self):
        a = auto.AutoLogger(TestAutoLogger.p, TestAutoLogger.test_number)
        os.makedirs(os.path.join(os.getcwd(), TestAutoLogger.test_number, '10a'))
        dir_name = a.generate_serial_number()
        self.assertEqual(dir_name, "01")
        shutil.rmtree(os.path.join(os.getcwd(), TestAutoLogger.test_number))

    def test_generate_serial_number__02(self):
        a = auto.AutoLogger(TestAutoLogger.p, TestAutoLogger.test_number)
        os.makedirs(os.path.join(os.getcwd(), TestAutoLogger.test_number, '01'))
        dir_name = a.generate_serial_number()
        self.assertEqual(dir_name, "02")
        shutil.rmtree(os.path.join(os.getcwd(), TestAutoLogger.test_number))

    def test_generate_serial_number__02_10a(self):
        a = auto.AutoLogger(TestAutoLogger.p, TestAutoLogger.test_number)
        os.makedirs(os.path.join(os.getcwd(), TestAutoLogger.test_number, '01'))
        os.makedirs(os.path.join(os.getcwd(), TestAutoLogger.test_number, '10a'))
        dir_name = a.generate_serial_number()
        self.assertEqual(dir_name, "02")
        shutil.rmtree(os.path.join(os.getcwd(), TestAutoLogger.test_number))

    def test_generate_serial_number__1000(self):
        a = auto.AutoLogger(TestAutoLogger.p, TestAutoLogger.test_number)
        os.makedirs(os.path.join(os.getcwd(), TestAutoLogger.test_number, '999'))
        dir_name = a.generate_serial_number()
        self.assertEqual(dir_name, "1000")
        shutil.rmtree(os.path.join(os.getcwd(), TestAutoLogger.test_number))

    def test_create_dir(self):
        a = auto.AutoLogger(TestAutoLogger.p, TestAutoLogger.test_number)
        path = a.create_dir()
        is_exists = os.path.exists(path)
        self.assertTrue(is_exists)
        shutil.rmtree(os.path.join(os.getcwd(), TestAutoLogger.test_number))

    @patch.object(os, 'makedirs', MagicMock())
    def test_create_dir_fail(self):
        a = auto.AutoLogger(TestAutoLogger.p, TestAutoLogger.test_number)
        self.assertRaises(IOError, a.create_dir)
        is_exists = os.path.exists(os.path.join(os.getcwd(), TestAutoLogger.test_number))
        self.assertFalse(is_exists)

    @patch.object(pexpect, 'spawn', MagicMock(return_value=MagicMock()))
    def test_start_script_cmd(self):
        a = auto.AutoLogger(TestAutoLogger.p, TestAutoLogger.test_number)
        ret = a.start_script_cmd()
        self.assertTrue(ret)

    @patch.object(pexpect, 'spawn', MagicMock(return_value=MagicMock()))
    @patch.object(remote, 'RemoteLogger', MagicMock())
    @patch.object(convert, 'Converter', MagicMock())
    def test_start(self):
        a = auto.AutoLogger(TestAutoLogger.p, TestAutoLogger.test_number)
        ret = a.start()
        self.assertTrue(ret)
        shutil.rmtree(os.path.join(os.getcwd(), TestAutoLogger.test_number))
