import os
import sys

SERVER_NAME      = 'depx.in'
# AWS_AUTH_URL     = f'https://api.{SERVER_NAME}/aws'
# AWS_AUTH_URL_DEV     = f'http://localhost:6000/aws'

# if os.environ.get("DEV") is not None:
#     COGNITO_CALLBACK = f'{AWS_AUTH_URL_DEV}/cognito-credentials/callback'
# else:
#     COGNITO_CALLBACK = f'{AWS_AUTH_URL}/cognito-credentials/callback'

if os.environ.get("DEV") is not None:
    # AWS_AUTH_URL     = f'http://localhost:6000/aws'
    AWS_AUTH_URL     = f'http://localhost:8000/csp/aws'
elif os.environ.get("STAGE") is not None:
    AWS_AUTH_URL     = f'https://staging-api.{SERVER_NAME}/csp/aws'
else:
    AWS_AUTH_URL     = f'https://api.{SERVER_NAME}/csp/aws'

# COGNITO_CALLBACK = f'{AWS_AUTH_URL}/cognito-credentials/callback'
COGNITO_CALLBACK = f'{AWS_AUTH_URL}/cognito-connect/callback'

if getattr(sys, 'frozen', False):
    USER_DATA_DIR = os.path.join(os.path.dirname(sys.executable), 'user_data')
    USER_EC2_DIR = os.path.join(os.path.dirname(sys.executable), 'ec2_key')
elif __file__:
    USER_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'user_data')
    USER_EC2_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ec2_key')

USER_DATA_JSON   = os.path.join(USER_DATA_DIR, 'user_data.json')

