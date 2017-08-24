#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import shutil
from unittest import TestCase

from logger import convert


class TestConverter(TestCase):
    def test_exec(self):
        p = convert.ConvertParams()
        p.script_path = "./tests/rule.csv"
        p.log_path = "./tests/test.tar.gz"

        ret = convert.Converter(p).exec()
        self.assertTrue(ret)
        with open("./tests/test.tar.conv/test.log", 'r') as f:
            for line in f.readlines():
                self.assertIsNotNone(re.match(".*★$", line))

        shutil.rmtree(os.path.join(os.getcwd(), "./tests/test.tar"))
        shutil.rmtree(os.path.join(os.getcwd(), "./tests/test.tar.conv"))

    def test_exec__file_not_found(self):
        p = convert.ConvertParams()
        p.script_path = "./rule.csv"
        p.log_path = "./tests/test.tar.gz"

        ret = convert.Converter(p).exec()
        self.assertFalse(ret)

    def test_exec__file(self):
        p = convert.ConvertParams()
        p.script_path = "./tests/rule.csv"
        p.file = "./tests/test.log"

        ret = convert.Converter(p).exec()
        self.assertTrue(ret)
        with open("./tests/test.conv.log", 'r') as f:
            for line in f.readlines():
                self.assertIsNotNone(re.match(".*★$", line))
        os.remove(os.path.join(os.getcwd(), "./tests/test.conv.log"))
