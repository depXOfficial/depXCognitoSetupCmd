import boto3

client = boto3.client("ec2", region_name='ap-south-1')

response = client.describe_key_pairs(
        KeyNames=[
            f'depx-ec2-keypair-123',
        ]
    )

print(response)