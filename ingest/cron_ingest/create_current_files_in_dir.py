import boto3
import os 
import botocore
import shutil

s3 = boto3.client('s3', endpoint_url="http://rook-ceph-rgw-nautiluss3.rook")

current_files_in_dir=[]

for obj in s3.list_objects_v2(Bucket="braingeneers-inbox")['Contents']:
    current_files_in_dir.append((obj['Key']).split('/')[0])

current_files_in_dir = list(set(current_files_in_dir))

current_files_in_dir.sort()

print(current_files_in_dir)

with open('current_files_in_dir.txt', 'w') as f:
    for item in current_files_in_dir:
        f.write("%s\n" % item)
