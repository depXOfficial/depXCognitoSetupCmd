import json

def create_identity_pool(client, user_pool_id, client_id, user_id):

    print("|--> Creating identity pool...")

    try:
        response = client.create_identity_pool(
            IdentityPoolName=f'depx-identity-pool-{user_id}',
            AllowUnauthenticatedIdentities=False,
            AllowClassicFlow=False,
            CognitoIdentityProviders=[
                {
                    'ProviderName': f'cognito-idp.ap-south-1.amazonaws.com/{user_pool_id}',
                    'ClientId': client_id,
                    'ServerSideTokenCheck': True
                },
            ]
        )

        return response['IdentityPoolId']

    except Exception as e:
        print("|--> An error occurred while creating Identity Pool: ", e)
        return None

def create_iam_role(client, identity_pool_id, user_id):

    print("|--> Creating IAM role...")

    try:
        trust = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Federated": "cognito-identity.amazonaws.com"
                    },
                    "Action": "sts:AssumeRoleWithWebIdentity",
                    "Condition": {
                        "StringEquals": {
                            "cognito-identity.amazonaws.com:aud": identity_pool_id
                        },
                        "ForAnyValue:StringLike": {
                            "cognito-identity.amazonaws.com:amr": "authenticated"
                        }
                    }
                }
            ]
        }

        response = client.create_role(
            Path='/depx/',
            RoleName=f'depx-role-{user_id}',
            AssumeRolePolicyDocument=json.dumps(trust),
            Description='role for depx app',
        )

        role_arn = response['Role']['Arn']
        role_name = response['Role']['RoleName']

        return role_arn, role_name

    except Exception as e:
        print("|--> An error occurred while creating IAM Role: ", e)
        return None, None

def attach_role_to_identity_pool(client, identity_pool_id, role_arn):

    print("|--> Attaching IAM role to Identity Pool...")

    try:
        response = client.set_identity_pool_roles(
            IdentityPoolId=identity_pool_id,
            Roles={
                'authenticated': role_arn
            }
        )

    except Exception as e:
        print("|--> An error occurred while attaching IAM Role to Identity Pool: ", e)

def identity_pool_exists(client, identity_pool_id):
    pool_exists = False
    next_token = None

    response = client.list_identity_pools(MaxResults=60)

    while True:
        # Check if the identity pool exists in the current batch
        for identity_pool in response['IdentityPools']:
            if identity_pool['IdentityPoolId'] == identity_pool_id:
                pool_exists = True
                break

        # Check if the identity pool was found or if there's more data to fetch
        if pool_exists or 'NextToken' not in response:
            break

        # Set the next token for the next iteration
        next_token = response['NextToken']
        response = client.list_identity_pools(MaxResults=60, NextToken=next_token)

    return pool_exists