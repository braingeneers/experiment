import boto3

# Create SQS client
sqs = boto3.client('sqs')

# List SQS queues
response = sqs.list_queues()

print(response['QueueUrls'])


# Create an SQS queue
response = sqs.create_queue(
    QueueName='SQS_QUEUE_NAME2',
    Attributes={
        'DelaySeconds': '60',
        'MessageRetentionPeriod': '86400'
    }
)

print(response['QueueUrl'])
