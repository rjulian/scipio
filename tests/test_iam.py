#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: test_example
.. moduleauthor:: Richard Julian <richard@rjulian.net>

This is a sample test module.
"""

import pytest
from moto import mock_iam
import scipio.aws_iam as iam
import scipio.aws as aws

"""
This is just an example test suite.  It will check the current project version
numbers against the original version numbers and will start failing as soon as
the current version numbers change.
"""

test_object = iam.AwsIam(aws.Aws())

@mock_iam
def test_privileged_user_creation():
    response = test_object.create_all_privileged_access()
    print(response)
    assert "User" in response
    assert "UserName" in response["User"]
    assert "scipio_run" in response["User"]["UserName"]
