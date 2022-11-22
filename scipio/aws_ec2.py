"""Module for handling core AWS ec2 functionality"""
import boto3

USERDATA_SCRIPT = """
echo "Hello logs."
"""
REGION = "us-east-1"
AMI_IMAGE_ID = "ami-08c40ec9ead489470"
INSTANCE_TYPE = "t2.micro"
DISK_SIZE_GB = 8
DEVICE_NAME = "/dev/xvda"
NAME = "scipio_run"
OWNER = "scipio"
RUNID = "ec2-1"
SUBNET_ID = "subnet-07cb1439"
SECURITY_GROUPS_IDS = ["sg-08e07cc9beb69d824"]
PUBLIC_IP = None
ROLE_PROFILE = "ec2-creator-role"


class AwsEc2:
    """Sets up AWS core ec2 functionality."""

    def __init__(self, aws_session):
        """New instance of AWS ec2 class"""
        self.aws_session = aws_session
        self.ec2_client = boto3.client("ec2")

    def simulate_mining_attack(self):
        """Undertakes launching of instance and malicious communication in userdata script."""
        blockDeviceMappings = [
            {
                "DeviceName": DEVICE_NAME,
                "Ebs": {
                    "DeleteOnTermination": True,
                    "VolumeSize": DISK_SIZE_GB,
                    "VolumeType": "gp2",
                },
            },
        ]
        response = self.ec2_client.run_instances(
            ImageId=AMI_IMAGE_ID,
            SubnetId=SUBNET_ID,
            SecurityGroupIds=SECURITY_GROUPS_IDS,
            UserData=USERDATA_SCRIPT,
            InstanceType=INSTANCE_TYPE,
            MinCount=1,
            MaxCount=1,
            BlockDeviceMappings=blockDeviceMappings,
            TagSpecifications=[
                {
                    "ResourceType": "instance",
                    "Tags": [
                        {"Key": "Name", "Value": NAME},
                        {"Key": "Owner", "Value": OWNER},
                        {"Key": "RunId", "Value": RUNID},
                    ],
                },
                {
                    "ResourceType": "volume",
                    "Tags": [
                        {"Key": "Name", "Value": NAME},
                        {"Key": "Owner", "Value": OWNER},
                        {"Key": "RunId", "Value": RUNID},
                    ],
                },
            ],
        )
        print(response)
