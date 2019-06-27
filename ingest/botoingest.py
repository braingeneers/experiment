import shutil
import os
import re
import sys
import glob
import json
import argparse
import datetime
import numpy as np
import boto3
import botocore
import read_data

#Established arguments. 
parser = argparse.ArgumentParser(
    description="Ingest a batch of experiments")
parser.add_argument('--issue', required=True,
                   help="Github issue is in internal")
args = parser.parse_args()

#Gets the current date
now = datetime.datetime.now()

#Establishes AWS Bucket
BUCKET_NAME = 'braingeneers-inbox' \
s3 = boto3.resource('s3')


#gets all the emails and makes directories with the names of the emails that put the files in
def download_directory_from_s3(bucketName,remoteDirectoryNames):
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucketName)

    for remoteDirectoryName in remoteDirectoryNames:
        
        for key in bucket.objects.filter(Prefix = remoteDirectoryName):
            

            if not os.path.exists(os.path.dirname(key.key)):
                os.makedirs(os.path.dirname(key.key))
          
            bucket.download_file(key.key,key.key)


remoteDirectories=['asrobbin@ucsc.edu']



formerPath=os.getcwd()
print("In Directory : " +os.getcwd())
path="%s/original" %str(os.getcwd())

#I am changing which directory I am in so I when I download the directories from AWS they will automatically go into "original"
os.chdir(path)
print("In Directory : " +os.getcwd())
#downloading directories into original
download_directory_from_s3(BUCKET_NAME,remoteDirectories)

#Change path back to normal
os.chdir(formerPath)
print("In Directory : "+ os.getcwd())



#renames all the directories into 0000-00-00-email for proper identification
for remoteDirectory in remoteDirectories:
    os.rename("original/{}".format(remoteDirectory),"original/{}".format(now.strftime("%Y-%m-%d")+"-"+remoteDirectory.partition("@")[0]))


# Batch = set of folders each with an experiment and all its recordings
for remoteDirectory in remoteDirectories:
    print("Ingesting batch {}".format(remoteDirectory))

    #deletes the directory for an ingest if the batch had been ingested before
    try:
        shutil.rmtree("derived/{}".format(now.strftime("%Y-%m-%d")+"-"+remoteDirectory.partition("@")[0], exist_ok=True))
    except OSError:
        pass
    
    #makes the directory with the correct identification(0000-00-00-email) in derived
    os.makedirs("derived/{}".format(now.strftime("%Y-%m-%d")+"-"+remoteDirectory.partition("@")[0], exist_ok=True))
    
    #declares batch_metadata
    batch_metadata = {
    "uuid": now.strftime("%Y-%m-%d")+"-"+ remoteDirectory.partition("@")[0],
    "issue": "https://github.com/braingeneers/internal/issues/{}".format(args.issue),
    "notes": open("original/{}/batch.txt".format(now.strftime("%Y-%m-%d")+"-"+remoteDirectory.partition("@")[0])).read() if os.path.exists(
        "original/{}/batch.txt".format(now.strftime("%Y-%m-%d")+"-"+remoteDirectory.partition("@")[0])) else ""}

experiments = []




# Get a list of all the experiments by extracting unique prefixes



for remoteDirectory in remoteDirectories:
    
    #Gets all the rhd files for a directory
    rhds = sorted(glob.glob("original/{}/*.rhd".format(now.strftime("%Y-%m-%d")+"-"+remoteDirectory.partition("@")[0], exist_ok=True)))
    #Gets all of the experiment names from the rhd files
    experiment_names = sorted(set(
        [re.findall(r"(.*?)\/(.*?)\/(.*?)_(\d{6}_\d{6}).rhd", s)[0][2] for s in rhds]))
    print("Experiment names:", experiment_names)



    for experiment_name in experiment_names:
        print("Ingesting experiment", experiment_name)

        experiment_metadata = {}

        experiment_metadata["name"] = experiment_name

    # Add <experiment_name>.txt to the notes field
        if os.path.exists("original/{}/{}.txt".format(now.strftime("%Y-%m-%d")+"-"+remoteDirectory.partition("@")[0], experiment_name)):
            experiment_metadata["notes"] = open(
                "original/{}/{}.txt".format(now.strftime("%Y-%m-%d")+"-"+remoteDirectory.partition("@")[0], experiment_name)).read()
        else:
            experiment_metadata["notes"] = ""

    # Find all the rhd's that match the experiment name and walk through in sorted/time order
        experiment_metadata["samples"] = []
        rhds = [p for p in sorted(glob.glob("original/{}/*.rhd".format(now.strftime("%Y-%m-%d")+"-"+remoteDirectory.partition("@")[0], exist_ok=True)))
                if re.findall(r"(.*?)\/(.*?)\/(.*?)_(\d{6}_\d{6}).rhd", p)[0][2] == experiment_name]

        print("Original rhd files to ingest:", rhds)

        for sample_path in rhds:
            print("Reading sample {}".format(sample_path))
            
        # Try reading its *.rhd file stopping if there is an error. Any earlier
        # samples in the run will be retained and stored but with an "error" field
        # in the experiments metadata
            data = read_data.read_data(sample_path)
            try:
                data = read_data.read_data(sample_path)
            except Exception as e:
                experiment_metadata["error"] = "{}: {}".format(sample_path, str(e))
                print("ERROR: {}".format(experiment_metadata["error"]))
                break
                
            sample_metadata = {}

            sample_metadata["num_samples"] = data["num_amplifier_samples"]

            sample_metadata["name"] = os.path.splitext(
                os.path.basename(sample_path).replace(" ", "-"))[0]

            sample_metadata["timestamp"] = datetime.datetime.strptime(
                re.findall(r"_(\d{6}_\d{6})", sample_metadata["name"])[0], "%y%m%d_%H%M%S").isoformat()
            print(sample_metadata["timestamp"])

            if "timestamp" not in batch_metadata:
                batch_metadata["timestamp"] = sample_metadata["timestamp"]
                
        # Add all the Intan metadata - < is a hack to exclude all sample data
            sample_metadata.update({k: v for k, v in data.items() if sys.getsizeof(v) < 2048})

            sample_metadata["original"] = sample_path
            sample_metadata["derived"] = "derived/{}/{}.npy".format(now.strftime("%Y-%m-%d")+"-"+remoteDirectory.partition("@")[0], sample_metadata["name"])

        # Save the original un-modified np.uint16 to save space and so there is no loss of accuracy
            sample_metadata["units"] = "µV"
            sample_metadata["offset"] = 32768
            sample_metadata["scaler"] = 0.195
            np.save(sample_metadata["derived"], data["amplifier_data"])

            experiment_metadata["samples"].append(sample_metadata)


    # Save the meta data for this experiment
        with open("derived/{}/{}.json".format(now.strftime("%Y-%m-%d")+"-"+remoteDirectory.partition("@")[0], experiment_metadata["name"]), "w") as f:
            json.dump(experiment_metadata, f, sort_keys=True)

        experiments.append({
            "path": "derived/{}/{}.json".format(now.strftime("%Y-%m-%d")+"-"+remoteDirectory.partition("@")[0], experiment_metadata["name"]),
            "timestamp": experiment_metadata["samples"][0]["timestamp"]
    })
    
# Add paths in timestamp order
batch_metadata["experiments"] = [
    e["path"] for e in sorted(experiments, key=lambda k: k['timestamp'], reverse=False)]

with open("derived/{}/metadata.json".format(now.strftime("%Y-%m-%d")+"-"+remoteDirectory.partition("@")[0], exist_ok=True), "w") as f:
    json.dump(batch_metadata, f, sort_keys=True)



for removeThis in remoteDirectories:
    try:
        shutil.rmtree(removeThis)
    except:
        pass

#for f in glob.glob("derived/{}".format(remoteDirectory)):
for remoteDirectory in remoteDirectories:
    if (len(os.listdir("derived/{}".format(now.strftime("%Y-%m-%d")+"-"+ remoteDirectory.partition("@")[0])))==1):
        shutil.rmtree("derived/{}".format(now.strftime("%Y-%m-%d")+"-"+ remoteDirectory.partition("@")[0]))

print("Finished ingesting batch.")
                                             
