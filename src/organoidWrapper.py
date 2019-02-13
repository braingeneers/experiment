#!/usr/bin/python
#usage python3 organoidWrapper.py 5001

#=====USAGE========================
# To run code locally:
# usage: python3 organoidWrapper.py runlocal
# Otherwise request defaults to run through AWS
#===================================

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import time
#import drywetlab

import sys
import os
import os.path
import PIL
import boto3
import json
#from PIL import Image
#-----------------------------------------------
import socket
import random
#from protocol import Message
import organoid
from organoid import OrganoidSim
#Usage: python3 organoidWrapper.py host port


def makeVideo():
    os.system("ffmpeg -r 3 -i figures/out/img%d.png -vcodec mpeg4 -y figures/movie.mp4")

def configuredExperiment(inputArray, filepath):
        #Iniialize Organoid
        sim = OrganoidSim(n=None, u=None, num_inputs=8, cam=None)
        seq_num = 0 #feedback loop sequence number

        #load numpy with pattern stimulation
        for input in inputArray:
            print("Input: ", input)
            pattern = input[0]
            #duration = input[1]
            print("Pattern ", seq_num, ": ", pattern)
            #Organoid Simulation
            sim.make_rob_a_picture(filepath+"out/", seq_num, 1000, 1100, pattern)
            sim.plot_stim(filepath+"stim/", seq_num, pattern=pattern, num_inputs=sim.u_width())

            seq_num+=1 #increment sequence number

        makeVideo()

def dynamicExperiment():
        return

def runLocal():
        return

def runWithAWS():
        return

def main():
        #if no ~/<GUID>.txt, generate guid
        #...
        #if no <GUID>queue on sqs, generate queue
        #...
        filepath = 'figures/'
        if (len(sys.argv) > 1 and sys.argv[1] == "runlocal"):
            int("Running Local!")
            f = "ec5600d8-17b5-45e5-93d6-2895119cb341.npy"
            inputArray = np.load(f)
            print(inputArray)
            configuredExperiment(inputArray, filepath)
            print("Done!")
            with open(e_guid + ".json", 'w') as fp:
                json.dump(data, fp)
        else:
            sqs = boto3.client('sqs')
            s3 = boto3.client('s3')
            bucket = 'katetemptestbucket'

            #find virtualExperimentQueues
            queues = sqs.list_queues(QueueNamePrefix='virtualExperimentQueue') # we filter to narrow down the list
            queue_url = queues['QueueUrls'][0]
            print(queue_url)

            while True:
                print("Getting message from sqs")
                # Get experiment request from queue
                messages = sqs.receive_message(QueueUrl=queue_url,MaxNumberOfMessages=1, WaitTimeSeconds=20) # adjust MaxNumberOfMessages if needed
                if 'Messages' in messages: # when the queue is exhausted response dict contains no 'Messages' key
                        message = messages['Messages'][0] # 'Messages' is a list
                        # process the messages
                        guid = message['Body']
                        print("Experiment guid:", guid)

                        #Get the experiment instructions json in s3
                        key_json = "experiments/" + guid + ".json"
                        f = s3.get_object(Bucket=bucket, Key=key_json)
                        data = json.load(f['Body'])

                        # Read json values
                        experiment = data["experiment"]
                        print(experiment)

                        # Delete the message from queue
                        sqs.delete_message(QueueUrl=queue_url,ReceiptHandle=message['ReceiptHandle'])

                        # Experiment configured or dynamic?
                        if(experiment["input"] == "configured"):
                            key_npy = "experiments/" + guid + ".npy"
                            print("Key:", key_npy)
                            f = guid + ".npy"
                            print("Local Filename:", f)
                            s3.download_file(bucket, key_npy, f)
                            print("Downloaded!")
                            inputArray = np.load(f)
                            print(inputArray)
                            configuredExperiment(inputArray, filepath)

                            #upload results to s3
                            path = os.getcwd() #get current working directory
                            for root,dirs,files in os.walk(path+"/figures"):
                                for file in files:
                                    s3.upload_file(os.path.join(root,file), bucket, "results/" + guid + "/" + file)

                            #Notify "Experiment Done" to AWS Lambda
                            done_queues = sqs.list_queues(QueueNamePrefix='requestCompleteQueue') # we filter to narrow down the list
                            done_queue_url = done_queues['QueueUrls'][0]
                            enqueue_response = sqs.send_message(QueueUrl=done_queue_url, MessageBody=guid)
                        else:
                            return
                else:
                    print("No requests, going to sleep...")
                    time.sleep(60)        #dynamicExperiment()



if __name__ == '__main__':
	  main()
