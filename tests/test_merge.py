#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from unittest import TestCase

from logger import merge, log


class TestMerge(TestCase):
    def test_exec(self):
        path = "tests/logs"
        out_path = path + merge.Merge.FILE_SUFFIX

        ret = merge.Merge().exec(path)

        self.assertTrue(ret)
        self.assertTrue(os.path.exists(out_path))
        os.remove(out_path)

    def test_exec__dirname(self):
        path = "tests/logs/"
        out_path = "tests/logs" + merge.Merge.FILE_SUFFIX

        ret = merge.Merge().exec(path)

        self.assertTrue(ret)
        self.assertTrue(os.path.exists(out_path))
        os.remove(out_path)

    def test_exec__dir_not_exists(self):
        path = "tests/not_exists_dir"
        log.set_level(log.Level.DEBUG)
        ret = merge.Merge().exec(path)
        self.assertFalse(ret)
