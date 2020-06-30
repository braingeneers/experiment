import boto3
import os
import botocore
import shutil
import logging
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3', endpoint_url=os.environ['ENDPOINT_URL'])

files_in_dir=[]

for obj in s3.list_objects_v2(Bucket="braingeneers-inbox")['Contents']:
    files_in_dir.append((obj['Key']).split('/')[0])

files_in_dir=list(set(files_in_dir))

files_in_dir.sort()

print(files_in_dir)
with open('files_in_dir.txt', 'w') as f:
    for item in files_in_dir:
        f.write("%s\n" % item)

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client= boto3.client('s3', endpoint_url=os.environ['ENDPOINT_URL'])
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

upload_file('files_in_dir.txt', 'braingeneers-inbox')
