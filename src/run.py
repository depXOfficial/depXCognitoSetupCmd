import os
import string
import random
import getpass
import json
import argparse

parser = argparse.ArgumentParser(description="Create new user credentials for Cognito")
parser.add_argument("-t", "--test", action="store_true", help="Test mode")

args = parser.parse_args()

if args.test:
    os.environ["DEV"] = "true"

import sys
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(current_dir)

from lib.cognito_idp.cognito_idp import (
    create_user_pool,
    create_user_pool_client,
    create_user_pool_domain,
    create_user_pool_user,
    set_user_pool_user_password
)

from lib.cognito_identity.cognito_identity import (
    create_identity_pool, 
    create_iam_role, 
    attach_role_to_identity_pool
)

from lib.iam.iam import (
    create_policy, 
    attach_policy_to_role
)

from lib.credentials.credentials import (
    store_aws_creds_in_env_variables, 
    store_credentials_from_file,
    check_credentials_validity_from_env
)

from lib.credentials.validate import validate_password, validate_email
from lib.ec2.ec2 import create_key_pair_ec2
from lib.cleanup.cleanup import cleanup
from lib.helpers.helpers import create_clients, generate_dashed_line

from lib.vars.vars import COGNITO_CALLBACK, USER_DATA_JSON, USER_DATA_DIR, USER_EC2_DIR
from lib.exceptions.exceptions import InvalidCSVFormat, InvalidCredentialsError

def create_new_user(
    cognito_idp_client, 
    cognito_identity_pool_client, 
    iam_client, ec2_client
):
    user_data = {}
    user_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=14))
    
    try:
        user_data["AwsCredsPath"] = os.environ.get('AWS_CREDENTIALS_PATH', None)

        username = input("Enter email (This will be your aws cognito username): ")
        while not validate_email(username):
            print("|--> Invalid email!")   
            username = input("\nEnter a valid email: ")

        password = getpass.getpass(prompt="Enter password: ")
        while not validate_password(password):
            print("|--> The password should have atleast one number, one uppercase letter, one lowercase letter, one special character and more than 8 characters")
            password = getpass.getpass(prompt="\nEnter password: ")

        reenter_password = getpass.getpass(prompt="Re-enter password: ")
        while password != reenter_password:
            print("|--> Passwords do not match!")
            reenter_password = getpass.getpass(prompt="Re-enter password: ")

        user_data["Email"] = username
        user_data["Password"] = password
        user_data["CognitoUserID"] = user_id
        

        user_data["CognitoUserPoolID"] = create_user_pool(cognito_idp_client, user_id)
        
        # callback_url = ""
        # if not prod:
        #     callback_url = COGNITO_CALLBACK_DEV
        # else:
        #     callback_url = COGNITO_CALLBACK
            
        user_data["CognitoUserPoolClientID"] = create_user_pool_client(cognito_idp_client, user_data["CognitoUserPoolID"], COGNITO_CALLBACK, user_id)
        user_data["CognitoUserPoolDomain"] = create_user_pool_domain(cognito_idp_client, user_data["CognitoUserPoolID"], user_id)
        
        create_user_pool_user(cognito_idp_client, user_data["CognitoUserPoolID"], username)
        set_user_pool_user_password(cognito_idp_client, user_data["CognitoUserPoolID"], username, password)

        user_data["IdentityPoolID"] = create_identity_pool(cognito_identity_pool_client, user_data["CognitoUserPoolID"], user_data["CognitoUserPoolClientID"], user_id)

        user_data["RoleArn"], user_data["RoleName"] = create_iam_role(iam_client, user_data["IdentityPoolID"], user_id)
        user_data["PolicyArn"] = create_policy(iam_client, user_id)
        attach_policy_to_role(iam_client, user_data["RoleName"], user_data["PolicyArn"])
        attach_role_to_identity_pool(cognito_identity_pool_client, user_data["IdentityPoolID"], user_data["RoleArn"])

        os.makedirs(USER_EC2_DIR, exist_ok=True)
        ec2_key_file = os.path.join(USER_EC2_DIR, f'depx-keypair-ec2-{user_id}.pem')
        keydata = create_key_pair_ec2(ec2_client, user_id)
        with open(ec2_key_file, 'w') as file:
            file.write(keydata)
        user_data["EC2KeyPairLoc"] = ec2_key_file

    except Exception as e:
        print("|--> Error: ", str(e))
        print("|--> Cleaning up....")
        cleanup(user_data)
        return None

    return user_data

if __name__ == "__main__":
    os.makedirs(USER_DATA_DIR, exist_ok=True)
        
    try:
        while True:
            print("\nChoose one of the following options:-\n")
            print("\t1. Create New User Credentials for Cognito")
            print("\n\t2. Set AWS Credentials Path")
            print("\t3. List stored values")
            print("\n\t4. Cleanup (Deletes UserPool, IdentityPool, Role and Policy created by the script)")
            print("\t5. Exit\n")
            option = input("Enter your choice: ")
            print("\n")


            if option == "1":
                try:
                    store_aws_creds_in_env_variables()
                except Exception as e:
                    print("|--> Error: ", str(e))
                    continue

                cognito_idp_client, cognito_identity_pool_client, iam_client, ec2_client = create_clients() 

                user_data = create_new_user(cognito_idp_client, cognito_identity_pool_client, iam_client, ec2_client)
                if user_data is not None:
                    print("\n")
                    generate_dashed_line()
                    print("\n")
                    print("Username         : ", user_data["Email"])
                    print("Password         : ", user_data["Password"])
                    print("CognitoUserID    : ", user_data["CognitoUserID"])
                    print("CognitoClientId  : ", user_data["CognitoUserPoolClientID"])
                    print("IdentityPoolId   : ", user_data["IdentityPoolID"])
                    print(f"\nNOTE: Make sure you change the permissions of the public key generated. \nRun the command: \"sudo chmod 600 {user_data['EC2KeyPairLoc']}\"")
                    print("\n")
                    generate_dashed_line()

                    file = open(USER_DATA_JSON)
                    vals = json.load(file)
                    file.close()

                    for key in user_data.keys():
                        if user_data[key] is not None:
                            vals[key] = user_data[key]

                    """ file = open(USER_DATA_JSON, 'w')
                    json.dump(vals, file)
                    file.close() """
                    with open(USER_DATA_JSON, 'w') as f:
                        json_str = json.dumps(vals)
                        f.write(json_str)
                        f.close()

            elif option == "2":
                print("|--> Setting AWS Credentials Path...")
                creds_path = input("\nEnter AWS CREDENTIALS absolute path: ")
                creds_path = creds_path.strip()

                while not os.path.exists(creds_path) or not os.path.isfile(creds_path) or creds_path == "" or creds_path == None:
                    error = f"|--> Invalid AWS CREDENTIALS PATH {creds_path}: "
                    
                    if creds_path == "":
                        error += "Cannot be empty!"
                    elif creds_path == None:
                        error += "Cannot be None!"
                    elif not os.path.exists(creds_path):
                        error += "Path does not exist!"
                    elif not os.path.isfile(creds_path):
                        error += "Path is not of a file!"

                    print(error)
                    creds_path = input("\nEnter correct AWS CREDENTIALS path: ")
                
                try:
                    store_credentials_from_file(creds_path)
                except InvalidCSVFormat:
                    print("|--> Invalid row format. Each row should have exactly 2 columns (Access Key, Secret Key).")
                except Exception as e:
                    print("|--> An error occurred: ", e)
                    continue

                if not check_credentials_validity_from_env():
                    continue

                print(f"\n|--> AWS CREDENTIALS PATH set to {creds_path}")

            elif option == "3":
                if not os.path.exists(USER_DATA_JSON):
                    print("|--> User data file not found")
                    continue

                print("\n|--> Listing stored values...\n")
                file = open(USER_DATA_JSON)
                vals = json.load(file)
                file.close()

                print("\n")
                generate_dashed_line()
                print("Username                 : ", vals['Email'])
                print("Password                 : ", vals['Password'])
                print("CognitoUserID            : ", vals['CognitoUserID'])
                print("CognitoUserPoolID        : ", vals['CognitoUserPoolID'])
                print("CognitoUserPoolClientID  : ", vals['CognitoUserPoolClientID'])
                print(f"CognitoUserPoolDomain    :  https://{vals['CognitoUserPoolDomain']}.auth.ap-south-1.amazoncognito.com")
                print("IdentityPoolID           : ", vals['IdentityPoolID'])
                print("RoleArn                  : ", vals['RoleArn'])
                print("RoleName                 : ", vals['RoleName'])
                print("PolicyArn                : ", vals['PolicyArn'])
                print("CredentialsFilepath      : ", vals['AwsCredsPath'])
                print("KeyPairLocation          : ", vals['EC2KeyPairLoc'])
                generate_dashed_line()
                print("\n")

            elif option == "4":
                try:
                    store_aws_creds_in_env_variables()
                except Exception as e:
                    print("|--> Error: ", str(e))
                    continue

                cognito_idp_client, cognito_identity_pool_client, iam_client, ec2_client = create_clients() 
        
                file = open(USER_DATA_JSON)
                cleanup(cognito_idp_client, cognito_identity_pool_client, iam_client, ec2_client, json.load(file))
                continue

            elif option == "5":
                print("|--> Exiting...\n")
                break

            else:
                print("|--> Invalid option!\n")
                continue

    except KeyboardInterrupt:
        print("\n\n|--> Exiting...\n")