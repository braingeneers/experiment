from __future__ import print_function

import json
import boto3

ses = boto3.client('ses')
s3 = boto3.client('s3')
sqs = boto3.client('sqs')

email_from = 'kvoitiuk@ucsc.edu'
emaiL_subject = 'AWS: File Uploaded to S3'


def lambda_handler(event, context):

    # Get the object from the event and show its name (should be json by trigger)
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Get the data from file
    f = s3.get_object(Bucket=bucket, Key=key)
    data = json.load(f['Body'])


    # Read json values
    experiment = data["experiment"]
    email_to = experiment["email"]


    #Distribute load------------------------------------

    #find correct queue
    if(experiment["type"] == "simulated"):
        queues = sqs.list_queues(QueueNamePrefix='virtualExperimentQueue') # we filter to narrow down the list
    else:
        queues = sqs.list_queues(QueueNamePrefix='realExperimentQueue') # we filter to narrow down the list

    queue_url = queues['QueueUrls'][0]


    #enqueue request
    enqueue_response = sqs.send_message(QueueUrl=queue_url, MessageBody=experiment["guid"])

    #----------------------------------------------------

    #augment json with organoid guid
    oguid = queue_url[queue_url.index("Queue")+len("Queue"):]
    experiment["oguid"] = oguid
    experiment["email"] = " "
    dest_bucket = 'braingeneers-providing'
    s3.put_object(Body=json.dumps(data), Bucket=dest_bucket, Key="experiment["guid"]/" + experiment["guid"] + ".json")


    #email (optional)---------------------------------------------------

    email_body = 'Success! Your experiment has been registered. \n\nExperiment GUID: ' + experiment["guid"] + '\n\nOrganoid: ' + oguid

    response = ses.send_email(
        Source = email_from,
        Destination={
            'ToAddresses': [
                email_to,
            ]
        },
        Message={
            'Subject': {
                'Data': emaiL_subject
            },
            'Body': {
                'Text': {
                    'Data': email_body
                }
            }
        }
    )
