import logging
import boto3
from botocore.exceptions import ClientError                                                              
import os                                                                                                
def get_list_of_files(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + get_list_of_files(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles
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
    s3_client = boto3.client('s3', endpoint_url=os.environ['ENDPOINT_URL'])
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
UUID=os.getenv('UUID')

if UUID[11] == 'e':
    path='/public/groups/braingeneers/ephys/'+UUID+'/blend_analysis/'
    files = get_list_of_files(path)

if UUID[11] == 'i':  
    path='/public/groups/braingeneers/imaging/'+UUID+'/blend_analysis/'
    files = get_list_of_files(path)

if UUID[11] == 'f': 
    path='/public/groups/braingeneers/fluidics/'+UUID+'/blend_analysis/' 
    files = get_list_of_files(path)

correct_files=[]

for file in files:
    print("Uploading", str(file), "to braingeneers/"+ str(file.split('braingeneers/')[1]))
    upload_file(file, 'braingeneers', file.split('braingeneers/')[1])


