import shutil
import os
import re
import sys
import glob
import json
import argparse
import datetime
import numpy as np

import read_data

parser = argparse.ArgumentParser(
    description="Ingest a batch of experiments")
#parser.add_argument('--uuid', required=True,
#                    help="UUID for batch")
parser.add_argument('--issue', required=True,
                   help="Github issue is in internal")
args = parser.parse_args()

import boto3
import botocore

now = datetime.datetime.now()

BUCKET_NAME = 'braingeneers-inbox' # replace with your bucket name

s3 = boto3.resource('s3')


#gets all the emails and makes a firectory wiht each which has ll the things in the directory
def download_directory_from_s3(bucketName,remoteDirectoryNames):
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucketName)

    for remoteDirectoryName in remoteDirectoryNames:
        #print(remoteDirectoryName)
        for key in bucket.objects.filter(Prefix = remoteDirectoryName):
            #print(key)

            if not os.path.exists(os.path.dirname(key.key)):
                os.makedirs(os.path.dirname(key.key))
          #  print("The Directory being made: "+ os.path.dirname(key.key) +" What is being downloaded in it: "+ key.key)
            bucket.download_file(key.key,key.key)

def copy_directory(src, dest):
    try:
        shutil.copytree(src, dest)
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)

remoteDirectories=['asrobbin@ucsc.edu']

formerPath=os.getcwd()
print("In Directory : " +os.getcwd())
path="%s/original" %str(os.getcwd())
os.chdir(path)
print("In Directory : " +os.getcwd())
download_directory_from_s3(BUCKET_NAME,remoteDirectories)
os.chdir(formerPath)
print("In Directory : "+ os.getcwd())
#for remoteDirectory in remoteDirectories:
 #   copy_directory(remoteDirectory,"original/{}".format(now.strftime("%Y-%m-%d")+"-"+remoteDirectory.partition("@")[0], exist_ok=True))



for remoteDirectory in remoteDirectories:
    os.rename("original/{}".format(remoteDirectory),"original/{}".format(now.strftime("%Y-%m-%d")+"-"+remoteDirectory.partition("@")[0]))


# Batch = set of folders each with an experiment and all its recordings
for remoteDirectory in remoteDirectories:
    print("Ingesting batch {}".format(remoteDirectory))

    #deletes the director if it already exists
    try:
        shutil.rmtree("derived/{}".format(now.strftime("%Y-%m-%d")+"-"+remoteDirectory.partition("@")[0], exist_ok=True))
    except OSError:
        pass
    #makes the directory with the guid
    os.makedirs("derived/{}".format(now.strftime("%Y-%m-%d")+"-"+remoteDirectory.partition("@")[0], exist_ok=True))
    #declares batch_metadata
    batch_metadata = {
    "uuid": now.strftime("%Y-%m-%d")+"-"+ remoteDirectory.partition("@")[0],
    "issue": "https://github.com/braingeneers/internal/issues/{}".format(args.issue),
    "notes": open("original/{}/batch.txt".format(now.strftime("%Y-%m-%d")+"-"+remoteDirectory.partition("@")[0])).read() if os.path.exists(
        "original/{}/batch.txt".format(now.strftime("%Y-%m-%d")+"-"+remoteDirectory.partition("@")[0])) else ""}

experiments = []



# # Add any metadata from json files to the batch metadata
# for f in glob.glob("original/{}/*.json".format(args.uuid)):
#     batch_metadata.update(json.load(open(f)))

# Ingest each experiment and exhaust in normalized form into derived/<args.uuid>/

# Get a list of all the experiments by extracting unique prefixes



for remoteDirectory in remoteDirectories:

    rhds = sorted(glob.glob("original/{}/*.rhd".format(now.strftime("%Y-%m-%d")+"-"+remoteDirectory.partition("@")[0], exist_ok=True)))
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
            
    # # Add any metadata from json files to the experiment metadata
    # for f in glob.glob("{}/*.json".format(original_path)):
    #     experiment_metadata.update(json.load(open(f)))

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

##for f in glob.glob("derived/{}".format(remoteDirectory)):
for remoteDirectory in remoteDirectories:
    if (len(os.listdir("derived/{}".format(now.strftime("%Y-%m-%d")+"-"+ remoteDirectory.partition("@")[0])))==1):
        shutil.rmtree("derived/{}".format(now.strftime("%Y-%m-%d")+"-"+ remoteDirectory.partition("@")[0]))

print("Finished ingesting batch.")
                                             
