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
import pickle
#from PIL import Image
#-----------------------------------------------
import socket
import random
#from protocol import Message
import organoid
from organoid import OrganoidSim
#Usage: python3 organoidWrapper.py host port
from os.path import expanduser


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

def findguid():
    home = expanduser("~")
    filepath = home + "/id.json" #id.json should be in homedirectory
    with open(filepath) as json_file:
        data = json.load(json_file)
    return data["resource"]["guid"]




def main():
            m_ip = "127.0.0.1"
            port = "5001"
            myguid = findguid()
            print("My guid is:", myguid)

            print ('Master ip:', m_ip, 'Port', port)
            s = socket.socket() #create socket
            port = int(port) #bind to port

    		# connect to server
            host_ip = socket.gethostbyname(str(m_ip))
            s.connect((host_ip, port))

            #while True:
            # send 8 bit number
            array = np.array([[1, 10], [2, 10], [4, 10]])
            print ('Original:')
            print(array)
            data = pickle.dumps(array)

            s.send(data)#str(random.randint(0,255)).encode('utf-8'))


            data = s.recv(4096) # receive echo from client
            data_array = pickle.loads(data)
            print ('Recieved:')
            print(data_array)#repr(data_array))
            print(data_array[0])
            time.sleep(1)

            #-----------------------------------------------
            s.close() #close socket
            #-----------------------------------------------
'''
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

            else:
                #dynamic experiment
                user_ip = experiment["client_ip"]
                user_port = int(experiment["client_port"])
                print(user_ip, user_port)
                return
'''


if __name__ == '__main__':
	  main()
