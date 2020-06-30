import boto3
import botocore
import os 
import shutil
import pickle
from zipfile import ZipFile

#KEY = 'my_image_in_s3.jpg' # replace with your object key

s3_client = boto3.client('s3', endpoint_url=os.environ['ENDPOINT_URL'])

#Function gets all the emails and makes a directory with the name of the email as the name of the directory
#----------------------------------------------------------------------------------------------

def download_directory_from_s3(bucketName,remoteDirectoryNames):
    s3_client = boto3.resource('s3', endpoint_url=os.environ['ENDPOINT_URL'])
    bucket = s3_client.Bucket(bucketName)

    for remoteDirectoryName in remoteDirectoryNames:
        #print(remoteDirectoryName)
        for key in bucket.objects.filter(Prefix = remoteDirectoryName):
            #print(key)

            if not os.path.exists(os.path.dirname(key.key)):
                os.makedirs(os.path.dirname(key.key))
            print("The Directory being made: "+ os.path.dirname(key.key) +" What is being downloaded in it: "+ key.key)
            bucket.download_file(key.key,key.key)
#---------------------------------------------------------------------------------------------------
UUID=os.getenv('UUID')

#with open ('uuid.txt', 'rb') as fp:
 #   uuid=str(pickle.load(fp))

remoteDirectoryNames = [UUID]

BUCKET_NAME = 'braingeneers-inbox'

#download_directory_from_s3(BUCKET_NAME, remoteDirectoryNames)

s3_client.download_file(BUCKET_NAME, UUID+'.zip', UUID+'.zip')

if not os.path.exists('/public/'):
    os.mkdir('/public/')

if not os.path.exists('/public/groups/'):
    os.mkdir('/public/groups/')

if not os.path.exists('/public/groups/braingeneers/'): 
    os.mkdir('/public/groups/braingeneers/')

if UUID[11]=='e':
    
    if not os.path.exists('/public/groups/braingeneers/ephys/'):
        os.mkdir('/public/groups/braingeneers/ephys/')

    with ZipFile(UUID+'.zip', 'r') as zipObj:
        zipObj.extractall('/public/groups/braingeneers/ephys/'+UUID+'/original/')

    print("Moving "+UUID+" to /public/groups/braingeneers/ephys/"+UUID+'/original/')

    
   #shutil.move(UUID, '/public/groups/braingeneers/ephys/'+UUID)

if UUID[11]=='i':
    if not os.path.exists('/public/groups/braingeneers/'):
        os.mkdir('/public/groups/braingeneers/imaging')

    with ZipFile(UUID+'.zip', 'r') as zipObj:
        zipObj.extractall('/public/groups/braingeneers/imaging/'+UUID+'/original/')

    print("Moving "+UUID+" to /public/groups/braingeneers/imaging/"+UUID+'/original/')

   # shutil.move(UUID, '/public/groups/braingeneers/imaging/'+UUID)

if UUID[11]=='f':
    if not os.path.exists('/public/groups/braingeneers/fluidics/'):
        os.mkdir('/public/groups/braingeneers/fluidics/')

    with ZipFile(UUID+'.zip', 'r') as zipObj:
        zipObj.extractall('/public/groups/braingeneers/fluidics/'+UUID+'/original/')

    print("Moving "+UUID+" to /public/groups/braingeneers/fluidics/"+UUID+'/original/')

    #shutil.move(UUID, '/public/groups/braingeneers/fluidics/'+UUID)







