#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: test_example
.. moduleauthor:: Richard Julian <richard@rjulian.net>

This is a sample test module.
"""

import pytest
import scipio.aws as aws

"""
This is just an example test suite.  It will check the current project version
numbers against the original version numbers and will start failing as soon as
the current version numbers change.
"""

def test_formatter_responds_correctly():
    sts_payload = {"Account": "1234567890", "Arn": "sample"}
    test_object = aws.Aws()
    formatted = test_object.format_sts_information(sts_payload)
    assert  "123456" in formatted


