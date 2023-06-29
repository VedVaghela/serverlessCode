import json
import boto3
import os

db_client = boto3.client('dynamodb')
sqs = boto3.client('sqs')
queue_url  = os.environ['SQS_URL']
dynamodb_name = os.environ['DYNAMO_DB_NAME']

def lambda_handler(event, context):
    #getting the Inactive account Ids from dynamodb
    response = db_client.scan(
        TableName=dynamodb_name,
        FilterExpression='#st = :s_val',
        ExpressionAttributeNames={
            "#st" : "Status"
        },
        ExpressionAttributeValues={
            ':s_val': {'S':'Inactive'}
        }
    )

    items = response['Items']
    for acc in items:
        #sending individual accounts to the queue        
        response_q = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        MessageAttributes={
            'AccountID': {
                'DataType': 'String',
                'StringValue': acc['AccountID']['S']
            }
        },
        MessageBody=(
            'Inactive account id info '
        )
        )

        print(response_q['MessageId'])

    return {
        'statusCode': 200,
        'body': json.dumps('All Inactive Account Ids Added into SQS queue')
    }
