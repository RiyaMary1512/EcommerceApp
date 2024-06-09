import json
import logging
import boto3
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize a session using Amazon DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TruckData')

def lambda_handler(event, context):
    logging.info(f"Received event: {json.dumps(event)}")
    
    try:
        # Parse the body of the event
        body = json.loads(event['body'])
        logging.info(f"Parsed body: {json.dumps(body)}")
        
        # Extract 'trucks' data
        trucks = body['trucks']
        logging.info(f"Extracted trucks data: {json.dumps(trucks)}")
        
        # Process the trucks data here
        for truck in trucks:
            logging.info(f"Processing truck data: {json.dumps(truck)}")
            
            # Put item into DynamoDB
            try:
                table.put_item(Item=truck)
                logging.info(f"Successfully inserted truck data: {truck['truck_id']}")
            except ClientError as e:
                logging.error(f"Failed to insert truck data: {e.response['Error']['Message']}")
                return {
                    'statusCode': 500,
                    'body': json.dumps({'error': f"Failed to insert truck data: {e.response['Error']['Message']}"})
                }
        
        # Return a successful response
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Data processed successfully'})
        }
    
    except KeyError as e:
        logging.error(f"KeyError: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f"KeyError: {str(e)}"})
        }
    
    except json.JSONDecodeError as e:
        logging.error(f"JSONDecodeError: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f"JSONDecodeError: {str(e)}"})
        }
    
    except Exception as e:
        logging.error(f"Exception: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Exception: {str(e)}"})
        }
