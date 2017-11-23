#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
from unittest import TestCase

from logger import convert


class TestConverter(TestCase):
    def test_exec(self):
        p = convert.ConvertParams()
        p.script_path = "./tests/rule.csv"
        p.log_path = "./tests/test.tar.gz"

        ret, _ = convert.Converter(p).exec()
        self.assertTrue(ret, True)

        num_line = sum(1 for line in open("./tests/test.tar.conv/test.log"))
        num_char = sum(line.count("★") for line in open("./tests/test.tar.conv/test.log"))
        self.assertEqual(num_line, num_char)

        shutil.rmtree(os.path.join(os.getcwd(), "./tests/test.tar"))
        shutil.rmtree(os.path.join(os.getcwd(), "./tests/test.tar.conv"))

    def test_exec__file_not_found(self):
        p = convert.ConvertParams()
        p.script_path = "./rule.csv"
        p.log_path = "./tests/test.tar.gz"

        ret, _ = convert.Converter(p).exec()
        self.assertFalse(ret)

    def test_exec__file(self):
        p = convert.ConvertParams()
        p.script_path = "./tests/rule.csv"
        p.file = "./tests/test.log"

        ret, _ = convert.Converter(p).exec()
        self.assertTrue(ret)

        num_line = sum(1 for line in open(p.file))
        num_char = sum(line.count("★") for line in open("./tests/test.conv.log"))
        self.assertEqual(num_line, num_char)

        os.remove(os.path.join(os.getcwd(), "./tests/test.conv.log"))

    def test_exec__file_regex(self):
        p = convert.ConvertParams()
        p.script_path = "./tests/regex.csv"
        p.file = "./tests/regex.log"

        ret, _ = convert.Converter(p).exec()
        self.assertTrue(ret)

        num_line = sum(1 for line in open(p.file))
        num_char = sum(line.count("★") for line in open("./tests/regex.conv.log"))
        self.assertEqual(num_line, num_char)

        os.remove(os.path.join(os.getcwd(), "./tests/regex.conv.log"))
