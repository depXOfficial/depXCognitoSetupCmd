from random import randint
import json
import boto3


def create_policy(client, user_id):

    print("|--> Creating IAM policy...")

    client = boto3.client("sts", region_name="ap-south-1")
    response = client.get_caller_identity()
    account_id = response["Account"]

    try:
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "VisualEditor0",
                    "Effect": "Allow",
                    "Action": [
                        "codepipeline:DeleteWebhook",
                        "codepipeline:ListPipelineExecutions",
                        "iam:RemoveRoleFromInstanceProfile",
                        "iam:CreateRole",
                        "cloudformation:DescribeStackResource",
                        "iam:AttachRolePolicy",
                        "autoscaling:*",
                        "iam:AddRoleToInstanceProfile",
                        "cloudformation:DescribeStackEvents",
                        "iam:DetachRolePolicy",
                        "elasticbeanstalk:DescribeEnvironments",
                        "iam:ListAttachedRolePolicies",
                        "codepipeline:ListPipelines",
                        "iam:ListPolicies",
                        "iam:GetRole",
                        "codepipeline:ListWebhooks",
                        "cloudformation:DescribeStackResources",
                        "iam:DeleteRole",
                        "cloudformation:DescribeStacks",
                        "elasticbeanstalk:ListPlatformVersions",
                        "elasticbeanstalk:CreateApplication",
                        "elasticbeanstalk:ListPlatformBranches",
                        "cloudwatch:*",
                        "elasticbeanstalk:CreateEnvironment",
                        "cloudformation:DeleteStack",
                        "ec2:*",
                        "iam:DeleteServiceLinkedRole",
                        "iam:CreateInstanceProfile",
                        "cognito-idp:GlobalSignOut",
                        "elasticbeanstalk:TerminateEnvironment",
                        "codepipeline:CreatePipeline",
                        "codepipeline:DeletePipeline",
                        "iam:ListInstanceProfilesForRole",
                        "cognito-idp:RevokeToken",
                        "elasticbeanstalk:DeleteApplication",
                        "elasticbeanstalk:DescribeApplications",
                        "iam:DeleteInstanceProfile",
                        "codepipeline:RegisterWebhookWithThirdParty",
                        "cloudformation:ListStacks",
                        "cognito-idp:GetUser",
                        "iam:GetInstanceProfile",
                        "s3:*",
                        "iam:ListRoles",
                        "elasticloadbalancing:*",
                        "iam:ListInstanceProfiles",
                        "elasticbeanstalk:ListAvailableSolutionStacks",
                        "iam:CreatePolicy",
                        "codepipeline:DeregisterWebhookWithThirdParty",
                        "iam:CreateServiceLinkedRole",
                        "cloudformation:CreateStack",
                        "sts:GetCallerIdentity",
                        "cognito-identity:GetCredentialsForIdentity",
                        "codepipeline:PutWebhook",
                    ],
                    "Resource": "*",
                },
                {
                    "Sid": "VisualEditor1",
                    "Effect": "Allow",
                    "Action": "iam:PassRole",
                    "Resource": [
                        "arn:aws:iam::231754098679:role/depx/*",
                        "arn:aws:iam::231754098679:instance-profile/depx/*",
                    ],
                },
            ],
        }

        response = client.create_policy(
            PolicyName=f"depx-policy-{user_id}",
            PolicyDocument=json.dumps(policy),
            Description="This policy gives permission to get credentials from web identity token",
        )

        policy_arn = response["Policy"]["Arn"]
        return policy_arn

    except Exception as e:
        print("|--> An error occurred while creating IAM Policy: ", e)


def attach_policy_to_role(client, role_name, policy_arn):

    print("|--> Attaching IAM policy to IAM role...")

    try:
        response = client.attach_role_policy(RoleName=role_name, PolicyArn=policy_arn)

        """ response = client.attach_role_policy(
            RoleName=role_name,
            PolicyArn="arn:aws:iam::aws:policy/AmazonEC2FullAccess"
        ) """

    except Exception as e:
        print("|--> An error occurred while attaching IAM Policy to IAM Role: ", e)


def iam_role_exists(client, role_name):
    role_exists = False
    next_token = None

    response = client.list_roles(MaxItems=60)

    while True:
        # Check if the identity pool exists in the current batch
        for roles in response["Roles"]:
            if roles["RoleName"] == role_name:
                role_exists = True
                break

        # Check if the identity pool was found or if there's more data to fetch
        if role_exists or "Marker" not in response:
            break

        # Set the next token for the next iteration
        next_token = response["Marker"]
        response = client.list_roles(MaxItems=60, Marker=next_token)

    return role_exists


def policy_exists(client, policy_arn):
    policy_exists = False
    next_token = None

    response = client.list_policies(Scope="Local", OnlyAttached=False, MaxItems=60)

    while True:
        # Check if the identity pool exists in the current batch
        for policies in response["Policies"]:
            if policies["Arn"] == policy_arn:
                policy_exists = True
                break

        # Check if the identity pool was found or if there's more data to fetch
        if policy_exists or "Marker" not in response:
            break

        # Set the next token for the next iteration
        next_token = response["Marker"]
        response = client.list_policies(
            Scope="Local", OnlyAttached=False, Marker=next_token, MaxItems=60
        )

    return policy_exists
