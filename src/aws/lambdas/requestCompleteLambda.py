from __future__ import print_function

import json
import boto3

ses = boto3.client('ses')
s3 = boto3.client('s3')
sqs = boto3.client('sqs')

email_from = 'kvoitiuk@ucsc.edu'
#email_cc = ''
emaiL_subject = 'AWS: File Uploaded to S3'
email_body = 'Success! The following file has been uploaded: '
bucket = 'braingeneers'
key = 'results/'

def lambda_handler(event, context):

    #parse sqs event on requestCompleteQueue

    key = 'results/' + guid + '.json'
    # Get the data from file
    f = s3.get_object(Bucket=bucket, Key=key)
    data = json.load(f['Body'])

    # Read json values
    experiment = data["experiment"]
    email_to = experiment["email"]

    #enqueue request



    response = ses.send_email(
        Source = email_from,
        Destination={
            'ToAddresses': [
                email_to,
            ],
#          'CcAddresses': [
#             email_cc,
#            ]
        },
        Message={
            'Subject': {
                'Data': emaiL_subject
            },
            'Body': {
                'Text': {
                    'Data': email_body + bucket + '/'+ key + '\n'
                }
            }
        }
    )
