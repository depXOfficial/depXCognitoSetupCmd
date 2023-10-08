from random import randint
import json

def create_policy(client, user_id):

    print("|--> Creating IAM policy...")

    try:
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "cognito-identity:GetCredentialsForIdentity"
                    ],
                    "Resource": [
                        "*"
                    ]
                },
                {
                    "Action": "ec2:*",
                    "Effect": "Allow",
                    "Resource": "*"
                },
                {
                    "Effect": "Allow",
                    "Action": "elasticloadbalancing:*",
                    "Resource": "*"
                },
                {
                    "Effect": "Allow",
                    "Action": "cloudwatch:*",
                    "Resource": "*"
                },
                {
                    "Effect": "Allow",
                    "Action": "autoscaling:*",
                    "Resource": "*"
                },
                {
                    "Effect": "Allow",
                    "Action": "iam:CreateServiceLinkedRole",
                    "Resource": "*",
                    "Condition": {
                        "StringEquals": {
                            "iam:AWSServiceName": [
                                "autoscaling.amazonaws.com",
                                "ec2scheduled.amazonaws.com",
                                "elasticloadbalancing.amazonaws.com",
                                "spot.amazonaws.com",
                                "spotfleet.amazonaws.com",
                                "transitgateway.amazonaws.com"
                            ]
                        }
                    }
                }
            ]
        }

        response = client.create_policy(
            PolicyName=f'depx-policy-{user_id}',
            PolicyDocument=json.dumps(policy),
            Description='This policy gives permission to get credentials from web identity token'
        )

        policy_arn = response['Policy']['Arn']
        return policy_arn

    except Exception as e:
        print("|--> An error occurred while creating IAM Policy: ", e)

def attach_policy_to_role(client, role_name, policy_arn):
    
    print("|--> Attaching IAM policy to IAM role...")

    try:
        response = client.attach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn
        )

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
        for roles in response['Roles']:
            if roles['RoleName'] == role_name:
                role_exists = True
                break

        # Check if the identity pool was found or if there's more data to fetch
        if role_exists or 'Marker' not in response:
            break

        # Set the next token for the next iteration
        next_token = response['Marker']
        response = client.list_roles(MaxItems=60, Marker=next_token)

    return role_exists

def policy_exists(client, policy_arn):
    policy_exists = False
    next_token = None

    response = client.list_policies(
        Scope='Local',
        OnlyAttached=False,
        MaxItems=60
    )

    while True:
        # Check if the identity pool exists in the current batch
        for policies in response['Policies']:
            if policies['Arn'] == policy_arn:
                policy_exists = True
                break
        
        # Check if the identity pool was found or if there's more data to fetch
        if policy_exists or 'Marker' not in response:
            break

        # Set the next token for the next iteration
        next_token = response['Marker']
        response = client.list_policies(
            Scope='Local',
            OnlyAttached=False,
            Marker=next_token,
            MaxItems=60
        )

    return policy_exists