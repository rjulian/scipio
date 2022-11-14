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
import os

os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"

"""
This is just an example test suite.  It will check the current project version
numbers against the original version numbers and will start failing as soon as
the current version numbers change.
"""

test_object = iam.AwsIam(aws.Aws())

@mock_iam
def test_user_creation():
    response = test_object.create_privileged_user()
    print(response)
    assert "User" in response
    assert "UserName" in response["User"]
    assert "scipio_user" in response["User"]["UserName"]

@mock_iam
def test_policy_creation():
    response = test_object.create_privileged_policy()
    print(response)
    assert "Policy" in response
    assert "scipio_policy" in response["Policy"]["PolicyName"]

@mock_iam
def test_policy_attachment():
    response = test_object.create_user_privileged_access()
    print(response)
    assert "HTTPStatusCode" in response["ResponseMetadata"]
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
