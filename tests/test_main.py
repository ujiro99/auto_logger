import unittest
from unittest import TestCase
from logger import auto
from logger.main import start, main

from click.testing import CliRunner
from unittest.mock import MagicMock, patch


class TestMain(TestCase):

    @patch.object(auto, 'AutoLogger', MagicMock(return_value=MagicMock()))
    @patch.object(auto.AutoLogger, 'finish', MagicMock(return_value=True))
    def test_start(self):
        runner = CliRunner()
        result = runner.invoke(start, ['-a', '192.168.1.2', '-t', '1-1-1'])
        self.assertEqual(result.exit_code, 0)

    @patch.object(auto, 'AutoLogger', MagicMock(return_value=MagicMock()))
    @patch.object(auto.AutoLogger, 'finish', MagicMock(return_value=False))
    def test_start_fail(self):
        runner = CliRunner()
        result = runner.invoke(start, ['-a', '192.168.1.2', '-t', '1-1-1'])
        self.assertEqual(result.exit_code, 0)

    def test_start_no_address(self):
        runner = CliRunner()
        result = runner.invoke(start, ['-t', '1-1-1'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'Error: addressを設定してください。\n')

    def test_start_no_testnumber(self):
        runner = CliRunner()
        result = runner.invoke(start, ['-a', '192.168.1.2'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'Error: test_numberを設定してください。\n')

    def test_main(self):
        with patch('logger.main.start'):
            main()

