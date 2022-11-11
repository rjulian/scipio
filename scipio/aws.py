"""Module for handling core AWS functionality"""
import boto3

class Aws:
    """Sets up AWS core functionality."""

    def __init__(self):
        """New instance of AWS class"""
        self.aws_session = None
        self.aws_client = None

    def display_configured_account(self):
        """Calls sts get caller identify and returns info for user."""
        self.aws_client = boto3.client('sts')
        caller_identity = self.aws_client.get_caller_identity()
        display_string = self.format_sts_information(caller_identity)
        return display_string

    def format_sts_information(self, caller_identity_payload):
        """Formats human readable response of STS info."""
        return f'''AWS Account ID: {caller_identity_payload["Account"]}
Full Caller ARN: {caller_identity_payload["Arn"]}'''
