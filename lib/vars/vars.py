import os
import sys

SERVER_NAME      = 'depx.in'
AWS_AUTH_URL     = f'https://api.{SERVER_NAME}/aws'
""" AWS_AUTH_URL     = f'http://localhost:6006/aws' """
COGNITO_CALLBACK = f'{AWS_AUTH_URL}/cognito-credentials/callback'

if getattr(sys, 'frozen', False):
    USER_DATA_DIR = os.path.join(os.path.dirname(sys.executable), 'user_data')
    USER_EC2_DIR = os.path.join(os.path.dirname(sys.executable), 'ec2_key')
elif __file__:
    USER_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'user_data')
    USER_EC2_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ec2_key')

USER_DATA_JSON   = os.path.join(USER_DATA_DIR, 'user_data.json')

