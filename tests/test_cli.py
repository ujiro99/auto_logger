from unittest import TestCase
from logger import auto
from logger.cli import start, main

from click.testing import CliRunner
from unittest.mock import MagicMock, patch


class TestMain(TestCase):

    @patch.object(auto.AutoLogger, 'execute', MagicMock(return_value=True))
    def test_start(self):
        runner = CliRunner()
        result = runner.invoke(start, ['-t', '1-1-1'])
        self.assertEqual(result.exit_code, 0)

    @patch.object(auto.AutoLogger, 'execute', MagicMock(return_value=False))
    def test_start_fail(self):
        runner = CliRunner()
        result = runner.invoke(start, ['-t', '1-1-1'])
        self.assertEqual(result.exit_code, 0)

    def test_start_no_testnumber(self):
        runner = CliRunner()
        result = runner.invoke(start)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'Error: test_numberを設定してください。\n')

    def test_main(self):
        with patch('logger.cli.start'):
            main()

