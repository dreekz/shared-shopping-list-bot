import json
import os
import boto3
from typing import Dict, Any, List, Optional
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext
from boto3.dynamodb.conditions import Key

logger = Logger()
tracer = Tracer()
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('DYNAMODB_TABLE', 'ShoppingList'))
users_table = dynamodb.Table(os.environ.get('USERS_TABLE', 'lists_users'))

@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """
    Main Lambda handler for shopping list operations.
    
    Args:
        event: API Gateway event
        context: Lambda context
    
    Returns:
        API Gateway response
    """
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        user_id = str(body.get('user_id'))
        
        # Verify user authorization
        if not is_user_authorized(user_id):
            return create_response(403, {'message': 'Unauthorized access'})

        # Handle different operations
        if 'action' in body and body['action'] == 'add_user':
            return handle_add_user(body)
            
        if event.get('httpMethod') == 'GET':
            return handle_list_items()
        elif event.get('httpMethod') == 'POST':
            return handle_add_item(body)
        elif event.get('httpMethod') == 'DELETE':
            return handle_remove_item(body)
        else:
            return create_response(400, {'message': 'Invalid operation'})

    except Exception as e:
        logger.exception('Error processing request')
        return create_response(500, {'message': f'Internal server error: {str(e)}'})

@tracer.capture_method
def is_user_authorized(user_id: str) -> bool:
    """Check if user is authorized to perform operations."""
    try:
        response = users_table.get_item(Key={'user_id': user_id})
        return 'Item' in response
    except Exception as e:
        logger.error(f'Error checking user authorization: {str(e)}')
        return False

@tracer.capture_method
def handle_list_items() -> Dict[str, Any]:
    """Handle GET request to list all items."""
    try:
        response = table.scan()
        items = response.get('Items', [])
        return create_response(200, {'items': items})
    except Exception as e:
        logger.error(f'Error listing items: {str(e)}')
        return create_response(500, {'message': 'Error retrieving items'})

@tracer.capture_method
def handle_add_item(body: Dict[str, Any]) -> Dict[str, Any]:
    """Handle POST request to add an item."""
    item_name = body.get('item_name')
    if not item_name:
        return create_response(400, {'message': 'Item name is required'})

    try:
        # Check if item already exists
        existing_items = table.scan(
            FilterExpression=Key('item_name').eq(item_name)
        )
        if existing_items.get('Items'):
            return create_response(409, {'message': 'Item already exists'})

        # Add new item
        table.put_item(Item={
            'list_id': f'item_{item_name.lower().replace(" ", "_")}',
            'item_name': item_name,
            'added_by': body.get('user_id')
        })
        return create_response(201, {'message': 'Item added successfully'})
    except Exception as e:
        logger.error(f'Error adding item: {str(e)}')
        return create_response(500, {'message': 'Error adding item'})

@tracer.capture_method
def handle_remove_item(body: Dict[str, Any]) -> Dict[str, Any]:
    """Handle DELETE request to remove an item."""
    item_name = body.get('item_name')
    if not item_name:
        return create_response(400, {'message': 'Item name is required'})

    try:
        # Find the item to delete
        existing_items = table.scan(
            FilterExpression=Key('item_name').eq(item_name)
        )
        if not existing_items.get('Items'):
            return create_response(404, {'message': 'Item not found'})

        # Delete the item
        item_id = existing_items['Items'][0]['list_id']
        table.delete_item(Key={'list_id': item_id})
        return create_response(200, {'message': 'Item removed successfully'})
    except Exception as e:
        logger.error(f'Error removing item: {str(e)}')
        return create_response(500, {'message': 'Error removing item'})

@tracer.capture_method
def handle_add_user(body: Dict[str, Any]) -> Dict[str, Any]:
    """Handle adding a new authorized user."""
    new_user_id = body.get('new_user_id')
    admin_id = body.get('user_id')

    try:
        # Verify admin status
        admin_response = users_table.get_item(Key={'user_id': admin_id})
        if not admin_response.get('Item', {}).get('is_admin', False):
            return create_response(403, {'message': 'Only admins can add users'})

        # Add new user
        users_table.put_item(Item={
            'user_id': new_user_id,
            'is_admin': False,
            'added_by': admin_id
        })
        return create_response(201, {'message': 'User added successfully'})
    except Exception as e:
        logger.error(f'Error adding user: {str(e)}')
        return create_response(500, {'message': 'Error adding user'})

def create_response(status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
    """Create standardized API response."""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body)
    }