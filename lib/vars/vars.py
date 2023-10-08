import os
import sys

SERVER_NAME      = 'depx.in'
AWS_AUTH_URL     = f'https://api.{SERVER_NAME}/aws'
COGNITO_CALLBACK = f'{AWS_AUTH_URL}/connect-cognito/callback'

if getattr(sys, 'frozen', False):
    USER_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(sys.executable)), 'user_data')
elif __file__:
    USER_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'user_data')

USER_DATA_JSON   = os.path.join(USER_DATA_DIR, 'user_data.json')