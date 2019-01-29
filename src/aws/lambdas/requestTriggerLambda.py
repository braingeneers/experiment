from __future__ import print_function

import json
#import urllib
#import urllib2
import boto3

ses = boto3.client('ses')

email_from = 'kvoitiuk@ucsc.edu'
#email_cc = ''
emaiL_subject = 'AWS: File Uploaded to S3'
email_body = 'Success! The following file has been uploaded: '



def lambda_handler(event, context):

    # Get the object from the event and show its namet
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    s3 = boto3.client('s3')
    data = s3.get_object(Bucket=bucket, Key=key)
    experiment = data['experiment'].read()

    #    data = json.load(f)
    #    experiment = data["experiment"]

    email_to = experiment["email"]

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
                    'Data': email_body + bucket + '/'+ key + '\n' +
                }
            }
        }
    )
