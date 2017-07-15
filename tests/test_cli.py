import click
from logger import auto, cli, params
from logger.cli import cmd, start, main, init

from unittest import TestCase
from click.testing import CliRunner
from unittest.mock import MagicMock, patch


class TestCli(TestCase):

    @patch.object(auto.AutoLogger, 'execute', MagicMock(return_value=True))
    def test_cmd(self):
        runner = CliRunner()
        result = runner.invoke(cmd, ['-t', '1-1-1'])
        self.assertEqual(result.exit_code, 0)

    @patch.object(auto.AutoLogger, 'execute', MagicMock(return_value=True))
    def test_cmd__start(self):
        runner = CliRunner()
        result = runner.invoke(cmd, ['start', '-t', '1-1-1'])
        self.assertEqual(result.exit_code, 0)

    @patch.object(auto.AutoLogger, 'execute', MagicMock(return_value=True))
    def test_start(self):
        runner = CliRunner()
        result = runner.invoke(start, ['-t', '1-1-1'])
        self.assertEqual(result.exit_code, 0)

    @patch.object(auto.AutoLogger, 'execute', MagicMock(return_value=False))
    def test_start__fail(self):
        runner = CliRunner()
        result = runner.invoke(start, ['-t', '1-1-1'])
        self.assertEqual(result.exit_code, 0)

    @patch.object(click, 'prompt', MagicMock(return_value=""))
    @patch.object(params.LogParam, 'write_ini', MagicMock(return_value="setting_file"))
    @patch.object(params.LogParam, 'read_ini', MagicMock(return_value=False))
    def test_start__init(self):
        runner = CliRunner()
        result = runner.invoke(start, ['-t', '1-1-1'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, '設定保存完了: setting_file\n')

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

