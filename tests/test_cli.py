#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import click
import configparser
from scripttest import TestFileEnvironment
from logger import auto, cli, params
from logger.cli import cmd, start, main, init
from logger.params import LogParam

from unittest import TestCase
from click.testing import CliRunner
from unittest.mock import MagicMock, patch


class TestCli(TestCase):

    @classmethod
    def setUpClass(cls):
        file_in_tests = os.path.join(os.getcwd(), 'tests', LogParam.FILE_NAME)
        file_current = os.path.join(os.getcwd(), LogParam.FILE_NAME)
        if not os.path.exists(file_current):
            shutil.copy(file_in_tests, file_current)

    @classmethod
    def tearDownClass(cls):
        file_current = os.path.join(os.getcwd(), LogParam.FILE_NAME)
        os.remove(file_current)

    @patch.object(auto.AutoLogger, 'start', MagicMock(return_value=True))
    def test_cmd(self):
        runner = CliRunner()
        result = runner.invoke(cmd, ['-t', '1-1-1'])
        self.assertEqual(result.exit_code, 0)

    @patch.object(auto.AutoLogger, 'start', MagicMock(return_value=True))
    def test_cmd__start(self):
        runner = CliRunner()
        result = runner.invoke(cmd, ['start', '-t', '1-1-1'])
        self.assertEqual(result.exit_code, 0)

    @patch.object(auto.AutoLogger, 'start', MagicMock(return_value=True))
    def test_start(self):
        runner = CliRunner()
        result = runner.invoke(start, ['-t', '1-1-1'])
        self.assertEqual(result.exit_code, 0)

    @patch.object(auto.AutoLogger, 'start', MagicMock(return_value=False))
    def test_start__fail(self):
        runner = CliRunner()
        result = runner.invoke(start, ['-t', '1-1-1'])
        self.assertEqual(result.exit_code, 0)

    @patch.object(click, 'prompt', MagicMock(return_value=""))
    @patch.object(params.LogParam, 'write_ini', MagicMock(return_value="setting_file"))
    @patch.object(params.LogParam, 'read_ini', MagicMock(return_value=False))
    @patch.object(auto.AutoLogger, 'start', MagicMock(return_value=True))
    def test_start__init(self):
        runner = CliRunner()
        result = runner.invoke(start, ['-t', '1-1-1'])
        self.assertEqual(result.exit_code, 0)
        self.assertRegex(result.output, '設定保存完了: setting_file.*')

    @patch.object(params.LogParam, 'write_ini', MagicMock(return_value="setting_file"))
    def test_init(self):
        args = [
            '--shell-cmd', 'telnet',
            '--host-name', '192.168.11.2',
            '--log-cmd', 'log_to_rom',
            '--remote-log-dir', '/home/user/log',
            '--remote-dist-dir', '/home/user/log_dist',
            '--local-src-dir', '/home/user/log_src']
        runner = CliRunner()
        result = runner.invoke(init, args)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, '設定保存完了: setting_file\n')

    def test_start__no_testnumber(self):
        runner = CliRunner()
        result = runner.invoke(start)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'Error: test-number を設定してください。\n')

    @patch.object(cli, 'cmd', MagicMock(return_value=True))
    def test_main(self):
        main()

    def test_script__start(self):
        env = TestFileEnvironment('./.tmp')

        ini = configparser.ConfigParser()
        ini[LogParam.DEFAULT] = {
            'host_name':       'root@172.30.10.2',
            'shell':           'ssh',
            'log_cmd':         'log_to_rom',
            'log_extension':   'tar.gz',
            'remote_log_dir':  '/root',
            'remote_dist_dir': '/mnt/src',
            'local_src_dir':   '../',
        }
        file_path = os.path.join(os.getcwd(), '.tmp', LogParam.FILE_NAME)
        with open(file_path, 'w') as file:
            ini.write(file)

        result = env.run('../logger/cli.py get', cwd='.tmp', expect_stderr=True)
        self.assertRegex(result.stdout, '正常に終了しました。')
        self.assertTrue(len(result.files_created) > 0)

