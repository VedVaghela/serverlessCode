import json
import boto3
import os

sqs = boto3.client('sqs')
queue_url  = os.environ['SQS_URL']

def lambda_handler(event, context):

    accountID = event['Records'][0]['dynamodb']['NewImage']['AccountID']['S']

    if event['Records'][0]['dynamodb']['NewImage']['Status']['S'] == 'Inactive':

        #send the changed id to queue
        response = sqs.send_message(
            QueueUrl=queue_url,
            DelaySeconds=10,
            MessageAttributes={
                'AccountID': {
                    'DataType': 'String',
                    'StringValue': accountID
                }
            },
            MessageBody=(
                'Inactive account id info '
            )
        )


    print('Status changed to ', event['Records'][0]['dynamodb']['NewImage']['Status']['S'])
    return {
        'statusCode': 200,
        'body': json.dumps('Status is changed in DynamoDB')
    }
