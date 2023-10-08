import os
from lib.cognito_idp.cognito_idp import (
    user_pool_exists
)

from lib.cognito_identity.cognito_identity import (
    identity_pool_exists
)

from lib.iam.iam import (
    iam_role_exists,
    policy_exists
)

from lib.ec2.ec2 import delete_key_pair_ec2, key_exists, delete_key_pair_ec2
from lib.helpers.helpers import create_clients

""" def cleanup(
        cognito_idp_client, cognito_identity_pool_client, 
        iam_client, ec2_client, vals
    ):

    non_none_keys = []

    # Loop through the dictionary
    for key, value in vals.items():
        if value is not None:
            non_none_keys.append(key)

    if 'user_pool_id' in non_none_keys:
        if user_pool_exists(cognito_idp_client, vals['user_pool_id']):
            if 'domain' in non_none_keys:
                print("|--> Deleting user pool domain...")
                response = cognito_idp_client.delete_user_pool_domain(
                    Domain=vals['domain'],
                    UserPoolId=vals['user_pool_id']
                )

            print("|--> Deleting user pool...")
            cognito_idp_client.delete_user_pool(UserPoolId=vals['user_pool_id'])
        else:
            print("|--> User pool doesn't exist or has already been deleted")        
        
    if 'identity_pool_id' in non_none_keys:
        if identity_pool_exists(cognito_identity_pool_client, vals['identity_pool_id']):
            print("|--> Deleting identity pool...")
            cognito_identity_pool_client.delete_identity_pool(IdentityPoolId=vals['identity_pool_id'])
        else:
            print("|--> Identity pool doesn't exist or has already been deleted")

    if 'policy_arn' in non_none_keys or 'role_name' in non_none_keys:
        if policy_exists(iam_client, vals['policy_arn']) and iam_role_exists(iam_client, vals['role_name']):
            print("|--> Detaching IAM policy from IAM role...")
            response = iam_client.detach_role_policy(
                RoleName=vals['role_name'],
                PolicyArn=vals['policy_arn']
            )
        else:
            print("|--> IAM policy or IAM role doesn't exist or has already been deleted")

        if policy_exists(iam_client, vals['policy_arn']):
            print("|--> Deleting IAM policy...")
            response = iam_client.delete_policy(
                PolicyArn=vals['policy_arn']
            )
        else:
            print("|--> IAM policy doesn't exist or has already been deleted")
        
        if iam_role_exists(iam_client, vals['role_name']):
            print("|--> Deleting IAM role...")
            iam_client.delete_role(RoleName=vals['role_name'])
        else:
            print("|--> IAM role doesn't exist or has already been deleted")

    if 'ec2_key_pair_location' in non_none_keys:
        if key_exists(ec2_client, vals['user_id']):
            delete_key_pair_ec2(ec2_client, vals['user_id'])
        else:
            print("|--> Key pair doesn't exist or has already been deleted") """


def cleanup(
    cognito_idp_client, 
    cognito_identity_pool_client, 
    iam_client, 
    ec2_client, 
    vals
):
    if 'CognitoUserPoolID' in vals:
        if user_pool_exists(cognito_idp_client, vals['CognitoUserPoolID']):
            if 'CognitoUserPoolDomain' in vals:
                print("|--> Deleting user pool domain...")
                response = cognito_idp_client.delete_user_pool_domain(
                    Domain=vals['CognitoUserPoolDomain'],
                    UserPoolId=vals['CognitoUserPoolID']
                )

            print("|--> Deleting user pool...")
            cognito_idp_client.delete_user_pool(UserPoolId=vals['CognitoUserPoolID'])
        else:
            print("|--> User pool doesn't exist or has already been deleted")        
        
    if 'IdentityPoolID' in vals:
        if identity_pool_exists(cognito_identity_pool_client, vals['IdentityPoolID']):
            print("|--> Deleting identity pool...")
            cognito_identity_pool_client.delete_identity_pool(IdentityPoolId=vals['IdentityPoolID'])
        else:
            print("|--> Identity pool doesn't exist or has already been deleted")

    if 'PolicyArn' in vals or 'RoleName' in vals:
        if policy_exists(iam_client, vals['PolicyArn']) and iam_role_exists(iam_client, vals['RoleName']):
            print("|--> Detaching IAM policy from IAM role...")
            response = iam_client.detach_role_policy(
                RoleName=vals['RoleName'],
                PolicyArn=vals['PolicyArn']
            )
        else:
            print("|--> IAM policy or IAM role doesn't exist or has already been deleted")

        if policy_exists(iam_client, vals['PolicyArn']):
            print("|--> Deleting IAM policy...")
            response = iam_client.delete_policy(
                PolicyArn=vals['PolicyArn']
            )
        else:
            print("|--> IAM policy doesn't exist or has already been deleted")
        
        if iam_role_exists(iam_client, vals['RoleName']):
            print("|--> Deleting IAM role...")
            iam_client.delete_role(RoleName=vals['RoleName'])
        else:
            print("|--> IAM role doesn't exist or has already been deleted")

    if 'EC2KeyPairLoc' in vals:
        if os.path.isfile(vals['EC2KeyPairLoc']):
            os.remove(vals['EC2KeyPairLoc'])
        if key_exists(ec2_client, vals['CognitoUserID']):
            delete_key_pair_ec2(ec2_client, vals['CognitoUserID'])
        else:
            print("|--> Key pair doesn't exist or has already been deleted")