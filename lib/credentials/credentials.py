import json
import boto3
import os
import csv

from lib.vars.vars import USER_DATA_DIR, USER_DATA_JSON
from lib.exceptions.exceptions import InvalidCSVFormat, InvalidCredentialsError

def validate_user_data_json(dir, path):
    os.makedirs(dir, exist_ok=True)

    if not os.path.exists(path):
        with open(path, 'w') as f:
            f.write(json.dumps({
                "description": "This file is used by depX Cognito Setup utitlity. Donot modify this file or risk breaking the app"
            }))
            f.close()
    
    return True

def store_aws_creds_in_env_variables():
    creds_path = os.environ.get('AWS_CREDENTIALS_PATH', None)
    if creds_path == None:
        if validate_user_data_json(USER_DATA_DIR, USER_DATA_JSON):
            f = open(USER_DATA_JSON, 'r')
            try:
                vals = json.load(f)
                creds_path = vals.get('AwsCredsPath', None)
                if creds_path != None and creds_path != '':
                    inp = input(f"Credentials file {creds_path} was found. Would you like to proceed with it? (y/n)(Default: y): ")
                    if inp == "n":
                        creds_path = input("\nEnter new credentials file path: ")
                        
                    if not check_credentials_validity_from_file(creds_path):
                        raise Exception("Credentials Invalid")
                                   
                    store_credentials_from_file(creds_path)
                    return
                        
                print("|--> AWS Credentials not found. Creating a new one...")
                creds_path = input("\nEnter new credentials file path: ")
                if not check_credentials_validity_from_file(creds_path):
                    raise Exception("Credentials Invalid")  
                                
                store_credentials_from_file(creds_path)
                return

            except json.JSONDecodeError:
                with open(USER_DATA_JSON, 'w') as f:
                    f.write(json.dumps({
                        "description": "This file is used by depX Cognito Setup utitlity. Donot modify this file or risk breaking the app"
                    }))
                    f.close()
                    return "User data contains an invalid json. Creating a new one"
                
            except Exception as e:
                return str(e)
        
def store_credentials_from_file(filename):
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        
        next(csv_reader)
        
        for row in csv_reader:

            if len(row) != 2:
                raise InvalidCSVFormat

            access_key = row[0].strip()
            secret_key = row[1].strip()

            os.environ['AWS_ACCESS_KEY_ID'] = access_key
            os.environ['AWS_SECRET_ACCESS_KEY'] = secret_key
            os.environ['AWS_CREDENTIALS_PATH'] = filename
    


def check_credentials_validity_from_env():
    try:
        print("|--> Checking credentials validity...")
        # Create a Boto3 client using the credentials
        client = boto3.client(
            'sts',
            region_name='ap-south-1',
            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
        )

        # Use the client to make a simple API call to AWS
        response = client.get_caller_identity()

        if not response['Arn']:
            raise InvalidCredentialsError

        # Print the response to indicate success and show some information
        print("|--> Credentials are valid.")
        print("\nAccount ID: ", response['Account'])
        print(f"User ARN: {response['Arn']}\n")

        return True

    except InvalidCredentialsError:
        print("|--> Credentials are invalid or an error occurred:")
        return False
    except Exception as e:
        print("|--> An error occurred: ", e)
        return False
    
def check_credentials_validity_from_file(filename):
    try:
        with open(filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            
            next(csv_reader)
            
            for row in csv_reader:

                if len(row) != 2:
                    raise InvalidCSVFormat

                access_key = row[0].strip()
                secret_key = row[1].strip()

                print("|--> Checking credentials validity...")
            # Create a Boto3 client using the credentials
            client = boto3.client(
                'sts',
                region_name='ap-south-1',
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key
            )

            # Use the client to make a simple API call to AWS
            response = client.get_caller_identity()

            if not response['Arn']:
                raise InvalidCredentialsError

            # Print the response to indicate success and show some information
            print("|--> Credentials are valid.")
            print("\nAccount ID: ", response['Account'])
            print(f"User ARN: {response['Arn']}\n")

            return True

    except InvalidCredentialsError:
        print("|--> Credentials are invalid or an error occurred:")
        return False
    except Exception as e:
        print("|--> An error occurred: ", e)
        return False