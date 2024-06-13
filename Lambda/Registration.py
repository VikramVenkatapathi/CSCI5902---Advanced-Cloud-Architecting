# {
#   "Name": "Name",
#   "Password": "Password",
#   "Email": "Email"
# }
import json
import boto3

aws_region = 'us-east-1'
dynamodb = boto3.resource('dynamodb', region_name=aws_region)
table_name = 'UserRegistration'

def lambda_handler(event, context):
    try:
        
        # Parse the request data
        registration_data = event
        name = registration_data.get('Name')
        password = registration_data.get('Password')
        email = registration_data.get('Email')

        # Validate the request data
        if not name or not password or not email:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',  # Allow requests from any origin
                    'Access-Control-Allow-Methods': 'OPTIONS,POST',  # Allow only specified methods
                    'Access-Control-Allow-Headers': 'Content-Type, ',  # Allow only specified headers
                },
                'body': json.dumps({'message': 'Invalid request data'}),
            }

        # Check if the email already exists in the DynamoDB table
        table = dynamodb.Table(table_name)
        response = table.get_item(Key={'Email': email})

        if 'Item' in response:
            # Item exists in DynamoDB
            return {
                'statusCode': 409,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',  # Allow requests from any origin
                    'Access-Control-Allow-Methods': 'OPTIONS,POST',  # Allow only specified methods
                    'Access-Control-Allow-Headers': 'Content-Type'  # Allow only specified headers
                },
                'body': json.dumps({'message': 'Email already exists'}),
            }

        # Add the registration information to the DynamoDB table
        table.put_item(Item={'Name': name, 'Password': password, 'Email': email})

        # Return a success response with CORS headers
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',  # Allow requests from any origin
                'Access-Control-Allow-Methods': 'OPTIONS,POST',  # Allow only specified methods
                'Access-Control-Allow-Headers': 'Content-Type',  # Allow only specified headers
            },
            'body': json.dumps({'message': 'Registration successful'}),
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
            'body': json.dumps({'message': 'Error occurred during registration', 'error': str(e)}),
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
