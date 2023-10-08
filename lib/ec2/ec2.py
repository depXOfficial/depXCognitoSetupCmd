import os

def create_key_pair_ec2(client, userid):
    print("|--> Creating keypair for EC2...")

    try:
        response = client.create_key_pair(
            KeyName=f'depx-ec2-keypair-{userid}',
            TagSpecifications=[
                {
                    'ResourceType': 'key-pair',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': f'depx-ec2-keypair-{userid}'
                        },
                    ]
                },
            ]
        )

        return response['KeyMaterial']
    
    except Exception as e:
        print("|--> An error occurred while creating keypair: ", e)
        return None


def delete_key_pair_ec2(client, userid):
    print("|--> Deleting keypair for EC2...")

    try:
        response = client.delete_key_pair(
            KeyName=f'depx-ec2-keypair-{userid}'
        )
    
    except Exception as e:
        print("|--> An error occurred while deleting keypair: ", e)


def key_exists(client, userid):
    try:
        response = client.describe_key_pairs(
            KeyNames=[
                f'depx-ec2-keypair-{userid}',
            ]
        )
        return True
    except:
        return False