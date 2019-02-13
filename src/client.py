#!/usr/bin/python

#=====USAGE========================
# To run code locally:
# usage: python3 client.py runlocal
# Otherwise request defaults to run through AWS
#===================================

import sys
import socket
import pickle
import random
import time
import json
import uuid #generate guids
import boto3
import numpy as np

#import protocol #defines internal Messaging format
#from protocol import Message


def main():
	#create experiment guid
	e_guid = str(uuid.uuid4())
	print("Experiment guid", e_guid)

	#Create experiment json
	data = {
		"experiment": {
			"guid": e_guid,
			"email": "kvoitiuk@ucsc.edu",
			"type": "simulated",
			"input": "configured",
			"date": "02-12-19"
	}}

	if(data["experiment"]["input"] == "dynamic"):
		data["experiment"]["client_ip"] = socket.gethostbyname(socket.gethostname())
		data["experiment"]["client_port"] = "5001"

	if(data["experiment"]["input"] == "configured"):
		x = np.array([[1, 10], [2, 10], [4, 10], [8, 10], [16, 10], [32, 10], [64, 10], [128, 10], [0, 10], [1, 10], [2, 10], [4, 10], [8, 10], [16, 10], [32, 10], [64, 10], [128, 10], [0, 10]])
		f= e_guid + ".npy"
		np.save(f, x)

	# Option to run on local computer with no connection to s3
	if (len(sys.argv) > 1 and sys.argv[1] == "runlocal"):
		print("Running Local!")
		with open(e_guid + ".json", 'w') as fp:
			json.dump(data, fp)
	else:
		#upload request to s3
		s3 = boto3.client('s3')
		bucket = 'braingeneers-receiving'
		#upload numpy to s3
		key_npy = e_guid + ".npy"
		s3.upload_file(f, bucket, key_npy)
		#upload main experiment request as json to s3, to activate trigger/request
		key_json = e_guid + ".json"
		s3.put_object(Body=json.dumps(data), Bucket=bucket, Key=key_json)


	if(data["experiment"]["input"] == "dynamic"): #for AI /interactive client
		#wait for organoid to connect to start dynamic communication
		#feedbackLoop()
		#???Message.announce(sys.argv[2], sys.argv[1], socket.gethostname(), Message.CLIENT, 5001)
		#???time.sleep(1)
		print("Dynamic!")

	#Otherise exit if experiment is configured
	print("Goodbye!")


if __name__ == '__main__':
	  main()
