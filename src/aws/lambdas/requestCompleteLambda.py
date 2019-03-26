from __future__ import print_function

import json
import boto3

ses = boto3.client('ses')
s3 = boto3.client('s3')
sqs = boto3.client('sqs')

email_from = 'kvoitiuk@ucsc.edu'
emaiL_subject = 'AWS: File Uploaded to S3'
dest_bucket = 'braingeneers-providing'
source_bucket = 'braingeneers-receiving'

def lambda_handler(event, context):

    #parse sqs event on requestCompleteQueue
    #deeplearning
    guid = event['Records'][0]['body']

    key_path = guid + '/'
    key = guid + '.json'

    link = 'https://s3-us-west-2.amazonaws.com/' + dest_bucket + '/' + key_path + 'data/movie.mp4'

    email_body = 'Results are ready for the following experiment:\n' + guid + '\n\nLink:\n' + link

    # Get email from original file
    f = s3.get_object(Bucket=source_bucket, Key=key)
    data = json.load(f['Body'])

    # Read json values
    experiment = data["experiment"]
    email_to = experiment["email"]


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
