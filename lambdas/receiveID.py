import json
import boto3
import os

sqs = boto3.client('sqs')
dynamodb = boto3.resource('dynamodb')
queue_url = os.environ['SQS_URL']
dynamoDB_name = os.environ['DYNAMO_DB_NAME']

def lambda_handler(event, context):

    # Receive message from SQS queue
    response_sqs = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )

    message = response_sqs['Messages'][0]
    receipt_handle = message['ReceiptHandle']
    accountIdForUpdate = message['MessageAttributes']['AccountID']['StringValue']

    #update dynamoDB before deletion from queue
    table = dynamodb.Table(dynamoDB_name)
    response_db = table.update_item(
        Key={
            'AccountID': accountIdForUpdate,
        },
        ExpressionAttributeNames={
            "#st" : "Status"
        },
        UpdateExpression='SET #st = :s_val',
        ExpressionAttributeValues={
            ':s_val': 'Active'
        }
    )
    # Delete element from queue
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )

    print('Received message & deleted: %s \n' % message )
    print('Item updated: ',response_db)

    return {
        'statusCode': 200,
        'body': accountIdForUpdate
    }
