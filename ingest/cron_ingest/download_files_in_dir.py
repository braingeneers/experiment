import boto3
import os 

s3 = boto3.client('s3', endpoint_url=os.environ['ENDPOINT_URL'])

s3.download_file('braingeneers-inbox', 'files_in_dir.txt', 'files_in_dir.txt')
