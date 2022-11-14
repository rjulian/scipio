"""Module for handling core AWS IAM functionality"""
import json
import uuid
import boto3

OVERPRIVILIGED_POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "IamAccess",
            "Effect": "Allow",
            "Action": [
                "iam:CreateUser",
                "iam:CreatePolicy",
                "iam:CreatePolicyVersion",
                "iam:SetDefaultPolicyVersion",
                "iam:AttachUserPolicy",
                "iam:AttachRolePolicy",
                "iam:AttachGroupPolicy",
            ],
            "Resource": ["*"],
        }
    ],
}


class AwsIam:
    """Sets up AWS core IAM functionality."""

    def __init__(self, aws_session):
        """New instance of AWS IAM class"""
        self.aws_session = aws_session
        self.iam_client = boto3.client("iam")
        self.iam_suffix = str(uuid.uuid4())[:8]

    def create_user_privileged_access(self):
        """Creates a user and policy in a way that would allow for privilege escalation."""
        policy_response = self.create_privileged_policy()
        user_response = self.create_privileged_user()
        policy_attach_response = self.attach_privileged_policy(
            policy_response["Policy"]["Arn"], user_response["User"]["UserName"]
        )
        return policy_attach_response

    def attach_privileged_policy(self, policy_arn, user_name):
        """Attaches policy to user that has been created."""
        print("Attaching policy to newly created user.")
        return self.iam_client.attach_user_policy(
            UserName=user_name, PolicyArn=policy_arn
        )

    def create_privileged_user(self):
        """Creates a user for access to privileged policy."""
        print(f"Creating user: scipio_user_{self.iam_suffix}")
        return self.iam_client.create_user(UserName=f"scipio_user_{self.iam_suffix}")

    def create_privileged_policy(self):
        """Creates policy with extra IAM privileges than needed."""
        print(f"Creating policy: scipio_policy_{self.iam_suffix}")
        return self.iam_client.create_policy(
            PolicyName=f"scipio_policy_{self.iam_suffix}",
            PolicyDocument=json.dumps(OVERPRIVILIGED_POLICY),
        )
