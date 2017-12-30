#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
from logging import StreamHandler
from unittest import TestCase

from logger import log


class TestLog(TestCase):
    def test_set_level(self):
        out = io.StringIO()
        log.logger.addHandler(StreamHandler(stream=out))
        log.set_level(log.Level.WARN)
        log.i("message")
        self.assertEqual(out.getvalue(), "")
        log.set_level(log.Level.INFO)
        log.i("message")
        self.assertEqual(out.getvalue(), "message\n")

    def test_d(self):
        out = io.StringIO()
        log.logger.addHandler(StreamHandler(stream=out))
        log.set_level(log.Level.DEBUG)

        log.d("message")
        self.assertEqual(out.getvalue(), "message\n")

    def test_d__byte(self):
        out = io.StringIO()
        log.logger.addHandler(StreamHandler(stream=out))
        log.set_level(log.Level.DEBUG)

        log.d(b'message')
        self.assertEqual(out.getvalue(), "message\n")

    def test_i(self):
        out = io.StringIO()
        log.logger.addHandler(StreamHandler(stream=out))

        log.i("message")
        self.assertEqual(out.getvalue(), "message\n")

    def test_w(self):
        out = io.StringIO()
        log.logger.addHandler(StreamHandler(stream=out))

        log.w("message")
        self.assertEqual(out.getvalue(), "message\n")

    def test_e(self):
        out = io.StringIO()
        log.logger.addHandler(StreamHandler(stream=out))

        log.e("message")
        self.assertEqual(out.getvalue(), "message\n")

    def test_color(self):
        log.d("debug")
        log.i("info")
        log.w("warn")
        log.e("error")

