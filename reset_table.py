import boto3
import time

def delete_table():
    # Use the same AWS credentials as your Lambda function
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # Make sure to use your region
    table_name = 'ShoppingList'
    
    print(f"Starting table reset process for {table_name}...")
    
    try:
        # Delete the table if it exists
        table = dynamodb.Table(table_name)
        print("Deleting existing table...")
        table.delete()
        
        # Wait for the table to be deleted
        print("Waiting for table deletion...")
        time.sleep(10)  # Give AWS some time
        
        # Create new table
        print("Creating new table...")
        dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'list_id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'list_id',
                    'AttributeType': 'S'
                }
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        
        print("Table reset completed successfully!")
        
    except Exception as e:
        print(f"Error during reset: {str(e)}")

if __name__ == "__main__":
    delete_table()