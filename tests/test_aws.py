#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: test_example
.. moduleauthor:: Richard Julian <richard@rjulian.net>

This is a sample test module.
"""

import pytest
from moto import mock_sts
import scipio.aws as aws

"""
This is just an example test suite.  It will check the current project version
numbers against the original version numbers and will start failing as soon as
the current version numbers change.
"""

test_object = aws.Aws()

def test_formatter_responds_correctly():
    sts_payload = {"Account": "1234567890", "Arn": "sample"}
    formatted = test_object.format_sts_information(sts_payload)
    assert "123456" in formatted

@mock_sts
def test_display_configured_account():
    display_string = test_object.display_configured_account()
    print(display_string)
    assert "Account" in display_string
    assert "arn:aws" in display_string
