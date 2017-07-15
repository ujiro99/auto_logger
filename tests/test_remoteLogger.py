import os
import shutil
import pexpect
from unittest import TestCase
from unittest.mock import MagicMock, patch

import logger.auto
from logger import remote


class TestRemoteLogger(TestCase):

    @patch.object(pexpect, 'spawn', MagicMock(return_value=MagicMock()))
    def test_get_log(self):
        params = logger.auto.LogParam()
        remote_logger = remote.RemoteLogger(params)
        remote_logger.get_log()

    def test_move_log(self):
        p = logger.auto.LogParam()
        p.local_src_dir = os.getcwd()
        p.local_dist_dir = os.path.join(os.getcwd(), "dist")

        # create src file, and dist directory
        filename = "testdata"
        f = open(os.path.join(os.getcwd(), filename), "w")
        f.close()
        os.mkdir(p.local_dist_dir)

        # exec
        remote_logger = remote.RemoteLogger(p)
        remote_logger.filename = filename
        ret = remote_logger.move_log()
        self.assertTrue(ret)

        is_exists = os.path.exists(os.path.join(p.local_dist_dir, filename))
        self.assertTrue(is_exists)
        shutil.rmtree(p.local_dist_dir)

    def test_move_log_timeout(self):
        p = logger.auto.LogParam()
        p.local_src_dir = os.getcwd()
        p.local_dist_dir = os.path.join(os.getcwd(), "dist")
        remote.RemoteLogger.TIMEOUT_MOVE = 1
        remote_logger = remote.RemoteLogger(p)
        remote_logger.filename = "testdata"
        ret = remote_logger.move_log()
        self.assertFalse(ret)
        is_exists = os.path.exists(os.path.join(p.local_dist_dir, remote_logger.filename))
        self.assertFalse(is_exists)
