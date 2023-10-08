from random import randint

read_attributes = [
    'address',	
    'birthdate',	
    'email',	
    'email_verified',	
    'family_name',	
    'gender',	
    'given_name',	
    'locale',	
    'middle_name',	
    'name',	
    'nickname',	
    'phone_number',	
    'phone_number_verified',	
    'picture',	
    'preferred_username',	
    'profile',	
    'updated_at',	
    'website',	
    'zoneinfo'
]

write_attributes = [
    'address',	
    'birthdate',	
    'email',		
    'family_name',	
    'gender',	
    'given_name',	
    'locale',	
    'middle_name',	
    'name',	
    'nickname',	
    'phone_number',		
    'picture',	
    'preferred_username',	
    'profile',	
    'updated_at',	
    'website',	
    'zoneinfo'
]

def create_user_pool(client, user_id):
    
    print("\n|--> Creating user pool...")

    try:
        response = client.create_user_pool(
            PoolName=f'depx-user-pool-{user_id}',
            UsernameAttributes=[
                'email',
            ],
            Policies={
                'PasswordPolicy': {
                    'MinimumLength': 8,
                    'RequireUppercase': True,
                    'RequireLowercase': True,
                    'RequireNumbers': True,
                    'RequireSymbols': True,
                    'TemporaryPasswordValidityDays': 7
                }
            },
            MfaConfiguration='OFF',
            AccountRecoverySetting={
                'RecoveryMechanisms': [
                    {
                        'Priority': 1,
                        'Name': 'admin_only'
                    },
                ]
            },
            AdminCreateUserConfig={
                'AllowAdminCreateUserOnly': True
            },
            VerificationMessageTemplate={
                'DefaultEmailOption': 'CONFIRM_WITH_LINK'
            },
            UserAttributeUpdateSettings={
                'AttributesRequireVerificationBeforeUpdate': [
                    'email'
                ]
            },
            Schema=[
                {
                    'Name': 'email',
                    'AttributeDataType': 'String',
                    'DeveloperOnlyAttribute': False,
                    'Mutable': True,
                    'Required': True,
                },
            ],
            EmailConfiguration={
                'EmailSendingAccount': 'COGNITO_DEFAULT'
            },
            AutoVerifiedAttributes=[
                'email'
            ],
        )

        user_pool_id = response['UserPool']['Id']
        return user_pool_id
    
    except Exception as e:
        print("|--> An error occurred while creating User Pool: ", e)
        return None

def create_user_pool_client(client, user_pool_id, callback_url, user_id):

    print("|--> Creating user pool client...")

    try:
        response = client.create_user_pool_client(
            UserPoolId=user_pool_id,
            ClientName=f'depx-pool-client-{user_id}',
            GenerateSecret=False,
            RefreshTokenValidity=30,
            AccessTokenValidity=60,
            IdTokenValidity=60,
            TokenValidityUnits={
                'AccessToken': 'minutes',
                'IdToken': 'minutes',
                'RefreshToken': 'days'
            },
            ExplicitAuthFlows=[
                'ALLOW_USER_PASSWORD_AUTH',
                'ALLOW_USER_SRP_AUTH',
                'ALLOW_REFRESH_TOKEN_AUTH',
            ],
            CallbackURLs=[
                callback_url,
            ],
            DefaultRedirectURI=callback_url,
            AuthSessionValidity=3,
            PreventUserExistenceErrors='ENABLED',
            EnableTokenRevocation=True,
            SupportedIdentityProviders=[
                'COGNITO',
            ],
            AllowedOAuthFlows=[
                'code',
            ],
            AllowedOAuthFlowsUserPoolClient=True,
            AllowedOAuthScopes=[
                'openid',
                'email',
            ],
            ReadAttributes=read_attributes,
            WriteAttributes=write_attributes,
        )
        
        client_id = response['UserPoolClient']['ClientId']
        return client_id

    except Exception as e:
        print("|--> An error occurred while creating User Pool Client: ", e)
        return None

def create_user_pool_domain(client, user_pool_id, user_id):

    print("|--> Creating user pool domain...")

    try:
        domain = f'depx-{user_id}'
        response = client.create_user_pool_domain(
            Domain=domain,
            UserPoolId=user_pool_id
        )

        return domain

    except Exception as e:
        print("|--> An error occurred while creating User Pool Domain: ", e)
        return None

def create_user_pool_user(client, user_pool_id, username):
    
    print("|--> Creating user pool user...")

    try:
        response = client.admin_create_user(
            UserPoolId=user_pool_id,
            Username=username,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': username
                },
                {
                    'Name': 'email_verified',
                    'Value': 'true'
                }
            ],
            TemporaryPassword='Testingpass@123',
            ForceAliasCreation=False,
            MessageAction='SUPPRESS'
        )

    except Exception as e:
        print("|--> An error occurred while creating User Pool User: ", e)

def set_user_pool_user_password(client, user_pool_id, username, password):

    print("|--> Setting user pool user password...")

    try:
        response = client.admin_set_user_password(
            UserPoolId=user_pool_id,
            Username=username,
            Password=password,
            Permanent=True
        )

    except Exception as e:
        print("|--> An error occurred while setting User Pool User Password: ", e)

def user_pool_exists(client, user_pool_id):
    pool_exists = False
    next_token = None

    response = client.list_user_pools(MaxResults=60)

    while True:
        # Check if the user pool exists in the current batch
        for user_pool in response['UserPools']:
            if user_pool['Id'] == user_pool_id:
                pool_exists = True
                break

        # Check if the user pool was found or if there's more data to fetch
        if pool_exists or 'NextToken' not in response:
            break

        # Set the next token for the next iteration
        next_token = response['NextToken']
        response = client.list_user_pools(MaxResults=60, NextToken=next_token)

    return pool_exists