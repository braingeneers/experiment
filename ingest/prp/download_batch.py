import boto3
import botocore                                                                                                                       
import os
import shutil                                                                                                                         
import pickle
BUCKET_NAME = 'braingeneers' # replace with your bucket name
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

os.mkdir('/public/')
os.mkdir('/public/groups/')  
os.mkdir('/public/groups/braingeneers/')

if UUID[11] == 'e':
    remoteDirectoryNames = ['ephys/'+UUID]
    download_directory_from_s3(BUCKET_NAME, remoteDirectoryNames)     
    os.mkdir('/public/groups/braingeneers/ephys')                                                                                   
    print("Moving "+UUID+" to /public/groups/braingeneers/ephys/"+UUID)                                                      
    shutil.move('ephys/'+UUID, '/public/groups/braingeneers/ephys/'+UUID)    

if UUID[11] == 'i': 
    remoteDirectoryNames = ['imaging/'+UUID] 
    download_directory_from_s3(BUCKET_NAME, remoteDirectoryNames)
    os.mkdir('/public/groups/braingeneers/imaging') 
    print("Moving "+UUID+" to /public/groups/braingeneers/imaging/"+UUID)
    shutil.move('imaging/'+UUID, '/public/groups/braingeneers/imaging/'+UUID)

if UUID[11] == 'f': 
    remoteDirectoryNames = ['fluidics/'+UUID]     
    download_directory_from_s3(BUCKET_NAME, remoteDirectoryNames)
    os.mkdir('/public/groups/braingeneers/fluidics')
    print("Moving "+UUID+" to /public/groups/braingeneers/fluidics/"+UUID)
    shutil.move('fluidics/'+UUID, '/public/groups/braingeneers/fluidics/'+UUID)  








