import boto3
import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
ADMIN_ID = os.getenv('ADMIN_ID')
# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('lists_users')  # Use the exact table name you created

# Replace this with your Telegram user ID
#ADMIN_ID = "YOUR_TELEGRAM_ID_HERE"  # Make sure to put your actual Telegram ID here

try:
    # Add admin user
    users_table.put_item(
        Item={
            'user_id': ADMIN_ID,
            'is_admin': True,
            'created_at': str(datetime.datetime.now())
        }
    )
    print(f"Successfully added admin user with ID: {ADMIN_ID}")
except Exception as e:
    print(f"Error adding admin user: {str(e)}")