import os
import shutil
from unittest import TestCase
from logger.params import LogParam


class TestLogParam(TestCase):

    buckup = 'plog.ini.bak'
    home = os.environ['HOME']
    current = os.getcwd()
    home_file = os.path.join(home, LogParam.FILE_NAME)
    home_backup = os.path.join(home, buckup)
    current_file = os.path.join(current, LogParam.FILE_NAME)
    current_backup = os.path.join(current, buckup)

    @classmethod
    def setUpClass(cls):
        if os.path.exists(cls.home_file):
            shutil.move(cls.home_file, cls.home_backup)
        if os.path.exists(cls.current_file):
            shutil.move(cls.current_file, cls.current_backup)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.home_backup):
            shutil.move(cls.home_backup, cls.home_file)
        if os.path.exists(cls.current_backup):
            shutil.move(cls.current_backup, cls.current_file)

    def test_read_ini__fail(self):
        if os.path.exists(TestLogParam.home_file):
            shutil.move(TestLogParam.home_file, TestLogParam.home_backup)
        if os.path.exists(TestLogParam.current_file):
            shutil.move(TestLogParam.current_file, TestLogParam.current_backup)
        p = LogParam()
        ret = p.read_ini()
        self.assertFalse(ret)

    def test_read_ini__current_directory(self):
        if os.path.exists(TestLogParam.home_file):
            shutil.move(TestLogParam.home_file, TestLogParam.home_backup)
        if os.path.exists(TestLogParam.current_backup):
            shutil.move(TestLogParam.current_backup, TestLogParam.current_file)
        p = LogParam()
        ret = p.read_ini()
        self.assertTrue(ret)

    def test_read_ini__home_directory(self):
        if os.path.exists(TestLogParam.current_file):
            shutil.move(TestLogParam.current_file, TestLogParam.current_backup)
        if os.path.exists(TestLogParam.current_backup):
            shutil.copy(TestLogParam.current_backup, TestLogParam.home_file)
        p = LogParam()
        ret = p.read_ini()
        self.assertTrue(ret)
        shutil.move(TestLogParam.home_file, TestLogParam.current_backup)

    def test_write_ini(self):
        if os.path.exists(TestLogParam.current_file):
            shutil.move(TestLogParam.current_file, TestLogParam.current_backup)
        if os.path.exists(TestLogParam.home_file):
            shutil.move(TestLogParam.home_file, TestLogParam.home_backup)

        p = LogParam()
        p.host_name = "host_name"
        p.shell = "shell"
        p.log_cmd = "log_cmd"
        p.remote_log_dir = "remote_log_dir"
        p.remote_dist_dir = "remote_dist_dir"
        p.local_src_dir = "local_src_dir"
        path = p.write_ini()
        self.assertEqual(path, os.path.join(os.environ['HOME'], LogParam.FILE_NAME))

        p2 = LogParam()
        p2.read_ini()
        self.assertEqual(p.host_name, p2.host_name)
        self.assertEqual(p.shell, p2.shell)
        self.assertEqual(p.log_cmd, p2.log_cmd)
        self.assertEqual(p.remote_log_dir, p2.remote_log_dir)
        self.assertEqual(p.remote_dist_dir, p2.remote_dist_dir)
        self.assertEqual(p.local_src_dir, p2.local_src_dir)

        os.remove(path)

