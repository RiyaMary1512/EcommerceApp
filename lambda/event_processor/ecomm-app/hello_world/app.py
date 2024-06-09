import json
import boto3
import logging
import base64
from botocore.exceptions import ClientError
from decimal import Decimal

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ProductViewTable')

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))
    
    for record in event['Records']:
        try:
            # Extract base64 encoded data from the Kinesis record
            encoded_data = record['kinesis']['data']
            logger.info("Encoded payload: %s", encoded_data)
            
            # Decode the base64 encoded data
            decoded_data = base64.b64decode(encoded_data).decode('utf-8')
            logger.info("Decoded payload: %s", decoded_data)
            
            # Parse the JSON payload
            payload = json.loads(decoded_data)
            logger.info("Parsed payload: %s", payload)
            
            # Extract details from payload
            product_id = payload.get('product_id')
            product_name = payload.get('product_name')
            click_count = payload.get('click_count')
            
            if not product_id or not product_name or click_count is None:
                raise KeyError("Missing required keys in payload data")
            
            # Update or insert item in DynamoDB
            response = table.update_item(
                Key={'product_id': product_id},
                UpdateExpression="SET product_name = :name, click_count = :count",
                ExpressionAttributeValues={
                    ':name': product_name,
                    ':count': click_count
                },
                ReturnValues="UPDATED_NEW"
            )
            
            logger.info("DynamoDB response: %s", json.dumps(response, cls=DecimalEncoder))
        
        except KeyError as e:
            logger.error("KeyError: %s", e)
        
        except ClientError as e:
            logger.error("ClientError: %s", e)
        
        except Exception as e:
            logger.error("Exception: %s", e)

    return {
        'statusCode': 200,
        'body': json.dumps('Successfully processed records')
    }

# Ensure the response from DynamoDB is JSON serializable
