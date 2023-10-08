import boto3
import os
import shutil

def create_clients():
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', None)
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)

    if AWS_ACCESS_KEY_ID == None or AWS_SECRET_ACCESS_KEY == None:
        print("|--> AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY not found!")
        exit(1)

    cognito_idp_client = boto3.client(
        'cognito-idp', 
        region_name='ap-south-1',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    cognito_identity_pool_client = boto3.client(
        'cognito-identity',
        region_name='ap-south-1',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    iam_client = boto3.client(
        'iam',
        region_name='ap-south-1',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    ec2_client = boto3.client(
        'ec2',
        region_name='ap-south-1',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    return cognito_idp_client, cognito_identity_pool_client, iam_client, ec2_client


def get_values_from_file():
    user_pool_id, client_id, domain = None, None, None 
    username, password, identity_pool_id = None, None, None
    role_arn, role_name, policy_arn = None, None, None
    domain, user_id, creds_path = None, None, None
    ec2_key_pair_loc = None
    
    with open('files/user_data.txt', 'r') as f:
        for line in f.readlines():
            data = line.strip().split(">>>>>>")

            if data[0].strip() == 'UserPoolId':
                user_pool_id = data[1].strip()
            elif data[0].strip() == 'ClientId':
                client_id = data[1].strip()
            elif data[0].strip() == 'Domain':
                domain = data[1].strip()
            elif data[0].strip() == 'Username':
                username = data[1].strip()
            elif data[0].strip() == 'Password':
                password = data[1].strip()
            elif data[0].strip() == 'IdentityPoolId':
                identity_pool_id = data[1].strip()
            elif data[0].strip() == 'RoleArn':
                role_arn = data[1].strip()
            elif data[0].strip() == 'RoleName':
                role_name = data[1].strip()
            elif data[0].strip() == 'PolicyArn':
                policy_arn = data[1].strip()
            elif data[0].strip() == 'depXUserID':
                user_id = data[1].strip()
            elif data[0].strip() == 'CredentialsFilepath':
                creds_path = data[1].strip()
            elif data[0].strip() == 'KeyPairLocation':
                ec2_key_pair_loc = data[1].strip()

    return {
        'user_pool_id': user_pool_id,
        'client_id': client_id,
        'domain': domain,
        'username': username,
        'password': password,
        'identity_pool_id': identity_pool_id,
        'role_arn': role_arn,
        'role_name': role_name,
        'policy_arn': policy_arn,
        'user_id': user_id,
        'creds_path': creds_path,
        'ec2_key_pair_location': ec2_key_pair_loc
    }


def generate_dashed_line():
    terminal_width = shutil.get_terminal_size().columns
    dashed_line = '-' * terminal_width
    print(dashed_line)