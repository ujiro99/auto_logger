import os
import shutil
import pexpect
from unittest import TestCase
from unittest.mock import MagicMock, patch

import logger.auto
import logger.params
from logger import remote, watch

class TestRemoteLogger(TestCase):

    @patch.object(pexpect, 'spawn', MagicMock(return_value=MagicMock))
    def test_get_log_timeout(self):
        params = logger.params.LogParam()
        remote_logger = remote.RemoteLogger(params)
        remote.RemoteLogger.TIMEOUT_LOGGING = 1

        p = pexpect.spawn()
        p.expect = MagicMock()
        p.send = MagicMock()
        p.match = MagicMock()
        p.terminate = MagicMock()
        array = [MagicMock()]
        p.match.groups = MagicMock(return_value=array)
        sentinel = "__tmp__.%s" % params.log_extension
        array[0].decode = MagicMock(return_value=sentinel)

        ret = remote_logger.get_log()
        self.assertFalse(ret)

    @patch.object(watch, 'file', MagicMock(return_value=True))
    def test_move_log(self):
        p = logger.params.LogParam()
        p.read_ini()
        p.local_src_dir = os.getcwd()
        p.local_dist_dir = os.path.join(os.getcwd(), "dist")

        # create src file, and dist directory
        filename = "testdata"
        f = open(os.path.join(os.getcwd(), filename), "w")
        f.close()
        if not os.path.exists(p.local_dist_dir):
            os.mkdir(p.local_dist_dir)

        # exec
        remote_logger = remote.RemoteLogger(p)
        remote_logger.filename = filename
        ret = remote_logger.move_log()
        self.assertTrue(ret)

        is_exists = os.path.exists(os.path.join(p.local_dist_dir, filename))
        self.assertTrue(is_exists)
        shutil.rmtree(p.local_dist_dir)

    @patch.object(watch, 'file', MagicMock(return_value=False))
    def test_move_log__timeout(self):
        p = logger.params.LogParam()
        p.read_ini()
        p.local_src_dir = os.getcwd()
        p.local_dist_dir = os.path.join(os.getcwd(), "dist")
        remote.RemoteLogger.TIMEOUT_MOVE = 1

        remote_logger = remote.RemoteLogger(p)
        remote_logger.filename = "testdata"
        ret = remote_logger.move_log()

        self.assertFalse(ret)
        is_exists = os.path.exists(os.path.join(p.local_dist_dir, remote_logger.filename))
        self.assertFalse(is_exists)
