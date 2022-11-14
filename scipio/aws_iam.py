"""Module for handling core AWS IAM functionality"""
import uuid
import boto3


class AwsIam:
    """Sets up AWS core IAM functionality."""

    def __init__(self, aws_session):
        """New instance of AWS IAM class"""
        self.aws_session = aws_session
        self.iam_client = boto3.client("iam")
        self.iam_suffix = str(uuid.uuid4())[:8]

    def create_all_privileged_access(self):
        """Creates policies, users, and roles in a way that would allow for privilege escalation."""
        print(f"Creating user: scipio_run_{self.iam_suffix}")
        return self.iam_client.create_user(UserName=f"scipio_run_{self.iam_suffix}")
