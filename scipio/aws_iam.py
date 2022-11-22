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
        # TODO remove in favor of aws_session.run_suffix
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

    def destroy_scipio_users_policies(self):
        """Deletes IAM resources created by scipio."""
        scipio_users = self.find_scipio_users()
        scipio_policies = self.find_scipio_policies()
        self.delete_users(scipio_users)
        self.delete_policies(scipio_policies)

    def delete_users(self, users):
        """Iterates over users, detaches policies, and deletes user"""
        for user in users:
            attached_policies = self.iam_client.list_attached_user_policies(
                UserName=user
            )
            for policy in attached_policies["AttachedPolicies"]:
                self.iam_client.detach_user_policy(
                    UserName=user, PolicyArn=policy["PolicyArn"]
                )
            self.iam_client.delete_user(UserName=user)

    def delete_policies(self, policies):
        """Deletes all policies passed in."""
        for policy in policies:
            self.iam_client.delete_policy(PolicyArn=policy)

    def find_scipio_policies(self):
        """Iterates over all policies, returning any including scipio prefix."""
        scipio_policies = []
        list_policies = self.iam_client.list_policies()
        policies = list_policies["Policies"]
        while "Marker" in list_policies:
            list_policies = self.iam_client.list_policies(
                Marker=list_policies["Marker"]
            )
            policies += list_policies["Policies"]
        for policy in policies:
            if "scipio_policy" in policy["PolicyName"]:
                scipio_policies.append(policy["Arn"])
        print(f"Found scipio policies: {scipio_policies}")
        return scipio_policies

    def find_scipio_users(self):
        """Iterates over all users, returning any including scipio prefix."""
        scipio_users = []
        list_users = self.iam_client.list_users()
        users = list_users["Users"]
        while "Marker" in list_users:
            list_users = self.iam_client.list_users(Marker=list_users["Marker"])
            users += list_users["Users"]
        for user in users:
            if "scipio_user" in user["UserName"]:
                scipio_users.append(user["UserName"])
        print(f"Found scipio users: {scipio_users}")
        return scipio_users
