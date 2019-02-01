#!/usr/bin/python

#=====ignore this comment for now===
#usage: python3 client.py host port
#example: python3 client.py localhost 5001
#======

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
from protocol import Message


def main():
	c#print(("Arg1: %s Arg2: %s" % (sys.argv[1], sys.argv[2])))
	s3 = boto3.client('s3')
	bucket = 'braingeneers'

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
			"date": "01-28-19"
	}}

	if(data["experiment"]["input"] == "dynamic"):
		data["experiment"]["client_ip"] = socket.gethostbyname(socket.gethostname())
		data["experiment"]["client_port"] = "5001"

	if(data["experiment"]["input"] == "configured"):
		x = np.array([[1, 10], [2, 10], [4, 10], [8, 10], [16, 10], [32, 10], [64, 10], [128, 10], [0, 10]])
		f= e_guid + ".npy"
		np.save(f, x)
		#upload numpy to s3
		key_npy = "experiments/" + e_guid + ".npy"
		s3.upload_file(f, bucket, key_npy)

	#upload main experiment request as json to s3, to activate trigger/request
	key_json = "experiments/" + e_guid + ".json"
	s3.put_object(Body=json.dumps(data), Bucket=bucket, Key=key_json)


	if(data["experiment"]["input"] == "dynamic"):
		#wait for organoid to connect to start dynamic communication
		#feedbackLoop()
		#???Message.announce(sys.argv[2], sys.argv[1], socket.gethostname(), Message.CLIENT, 5001)
		#???time.sleep(1)
		print("Dynamic!")

	#Otherise exit if experiment is configured
	print("Goodbye!")


if __name__ == '__main__':
	  main()
