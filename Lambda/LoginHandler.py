# {
#     "Password": "Password",
#     "Email": "Email"
# }

import json
import boto3

# AWS configuration
aws_region = 'us-east-1'
dynamodb = boto3.resource('dynamodb', region_name=aws_region)
table_name = 'UserRegistration'

# Content-Type,Authorization
def lambda_handler(event, context):
    try:
        # Parse the request data
        login_data = event
        email = login_data.get('Email')
        password = login_data.get('Password')

        # Validate the request data
        if not email or not password:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',  # Allow requests from any origin
                    'Access-Control-Allow-Methods': 'OPTIONS,POST',  # Allow only specified methods
                    'Access-Control-Allow-Headers': 'Content-Type',  # Allow only specified headers
                },
                'body': json.dumps({'message': 'Invalid request data'}),
            }

        # Check if the email exists in the DynamoDB table
        table = dynamodb.Table(table_name)
        response = table.get_item(Key={'Email': email})

        if 'Item' not in response:
            # Email does not exist in DynamoDB
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',  # Allow requests from any origin
                    'Access-Control-Allow-Methods': 'OPTIONS,POST',  # Allow only specified methods
                    'Access-Control-Allow-Headers': 'Content-Type',  # Allow only specified headers
                },
                'body': json.dumps({'message': 'Email not found'}),
            }

        # Verify the password
        user_data = response['Item']
        if user_data['Password'] != password:
            # Incorrect password
            return {
                'statusCode': 401,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',  # Allow requests from any origin
                    'Access-Control-Allow-Methods': 'OPTIONS,POST',  # Allow only specified methods
                    'Access-Control-Allow-Headers': 'Content-Type',  # Allow only specified headers
                },
                'body': json.dumps({'message': 'Incorrect password'}),
            }

        # Successful login with CORS headers
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',  # Allow requests from any origin
                'Access-Control-Allow-Methods': 'OPTIONS,POST',  # Allow only specified methods
                'Access-Control-Allow-Headers': 'Content-Type',  # Allow only specified headers
            },
            'body': json.dumps({'message': 'Login successful'}),
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',  # Allow requests from any origin
                'Access-Control-Allow-Methods': 'OPTIONS,POST',  # Allow only specified methods
                'Access-Control-Allow-Headers': 'Content-Type',  # Allow only specified headers
            },
            'body': json.dumps({'message': 'Error occurred during login', 'error': str(e)}),
        }

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',  # Allow requests from any origin
            'Access-Control-Allow-Methods': 'OPTIONS,POST',  # Allow only specified methods
            'Access-Control-Allow-Headers': 'Content-Type',  # Allow only specified headers
        },
        'body': json.dumps('Hello from Lambda!'),
    }
