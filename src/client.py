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






        '''
    		while True:
    			# receive 8 bit number from client
    			input = c.recv(128)
    			print("Master sent: ")
    			print(str(input))
    			# echo 8 bit number
    			c.send(input)

    			#Organoid Simulation
    			pattern = int(input)
    			i = seq_num
    			sim.make_rob_a_picture('figures/', seq_num, 1000, 1100, pattern)
    			sim.plot_stim('figures/', seq_num, pattern=pattern, num_inputs=sim.u_width())

    			seq_num+=1 #increment sequence number
        '''


    '''
        filepath = 'figures/'
        if (len(sys.argv) > 1 and sys.argv[1] == "runlocal"):
            runLocal()

        else:
            sqs = boto3.resource('sqs')
            s3 = boto3.resource('s3')

            myguid = findguid()
            print("My guid is: ", myguid)
            queue_name = experiment_type + "Queue" + myguid

            #check if <GUID>queue is on sqs
            try:
                queue = sqs.get_queue_by_name(QueueName=queue_name) # we filter to narrow down the list
            except:
                #create <GUID>queue
                print("No queue found! Creating queue...")
                queue = sqs.create_queue(QueueName=queue_name) # we filter to narrow down the list
                print(queue.url)
            exit()

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
                        key_json = guid + ".json"
                        f = s3.get_object(Bucket=source_bucket, Key=key_json)
                        data = json.load(f['Body'])

                        # Read json values
                        experiment = data["experiment"]
                        print(experiment)

                        # Delete the message from queue
                        sqs.delete_message(QueueUrl=queue_url,ReceiptHandle=message['ReceiptHandle'])

                        # Experiment configured or dynamic?
                        if(experiment["input"] == "configured"):
                            key_npy = guid + ".npy"
                            print("Key:", key_npy)
                            f = guid + ".npy"
                            print("Local Filename:", f)
                            s3.download_file(source_bucket, key_npy, f)
                            print("Downloaded!")
                            inputArray = np.load(f)
                            print(inputArray)
                            configuredExperiment(inputArray, filepath)

                            #upload results to s3
                            path = os.getcwd() #get current working directory
                            for root,dirs,files in os.walk(path+"/figures"):
                                for file in files:
                                    s3.upload_file(os.path.join(root,file), dest_bucket, guid + "/" + "data" + "/" + file)

                            #Notify "Experiment Done" to AWS Lambda
                            done_queues = sqs.list_queues(QueueNamePrefix='requestCompleteQueue') # we filter to narrow down the list
                            done_queue_url = done_queues['QueueUrls'][0]
                            enqueue_response = sqs.send_message(QueueUrl=done_queue_url, MessageBody=guid)
                        else:
                            #dynamic experiment
                            user_ip = experiment["client_ip"]
                            user_port = int(experiment["client_port"])
                            print(user_ip, user_port)
                            return

                else:
                    print("No requests, going to sleep...")
                    time.sleep(60)
    '''
