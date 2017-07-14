import os
import pexpect
import shutil
from unittest import TestCase
from unittest.mock import MagicMock, patch
from logger import auto, remote


class TestAutoLogger(TestCase):

    address = "192.168.1.2"
    test_number = "1-1-1"

    def test_generate_date_str(self):
        a = auto.AutoLogger(TestAutoLogger.address, TestAutoLogger.test_number)
        date_str = a.generate_date_str()
        self.assertRegex(date_str, "\d\d-\d\d-\d\d_\d\d\d\d\d\d")

    def test_create_dir(self):
        a = auto.AutoLogger(TestAutoLogger.address, TestAutoLogger.test_number)
        path = a.create_dir()
        is_exists = os.path.exists(path)
        self.assertTrue(is_exists)
        shutil.rmtree(os.path.join(os.getcwd(), TestAutoLogger.test_number))

    @patch.object(os, 'makedirs', MagicMock())
    def test_create_dir_fail(self):
        a = auto.AutoLogger(TestAutoLogger.address, TestAutoLogger.test_number)
        self.assertRaises(IOError, a.create_dir)
        is_exists = os.path.exists(os.path.join(os.getcwd(), TestAutoLogger.test_number))
        self.assertFalse(is_exists)

    @patch.object(pexpect, 'spawn', MagicMock(return_value=MagicMock()))
    def test_start(self):
        a = auto.AutoLogger(TestAutoLogger.address, TestAutoLogger.test_number)
        ret = a.start()
        self.assertTrue(ret)
        shutil.rmtree(os.path.join(os.getcwd(), TestAutoLogger.test_number))

    @patch.object(pexpect, 'spawn', MagicMock(return_value=MagicMock()))
    @patch.object(remote, 'RemoteLogger', MagicMock())
    def test_finish(self):
        a = auto.AutoLogger(TestAutoLogger.address, TestAutoLogger.test_number)
        ret = a.finish()
        self.assertTrue(ret)

