#!/usr/bin/python
#usage python3 organoidWrapper.py 5001

#=====USAGE========================
# To run code locally:
# usage: python3 master.py runlocal
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
        print("Running Local!")
        f = "ec5600d8-17b5-45e5-93d6-2895119cb341.npy"
        inputArray = np.load(f)
        print(inputArray)
        configuredExperiment(inputArray, filepath)
        print("Done!")
        with open(e_guid + ".json", 'w') as fp:
            json.dump(data, fp)
        return

def runWithAWS():
        return

def findguid():
    filepath = "../../guid.txt"
    fd = open(filepath, "r")
    return fd.readline().rstrip('\n')


source_bucket = 'braingeneers-receiving'
dest_bucket = 'braingeneers-providing'
experiment_type = "virtualExperiment"




def main():
        ip = "127.0.0.1"
        port = "5001"
        print ('My ip:', ip, 'My port', port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket
        port = int(port) #bind to port
        s.bind(('', port)) #bind to port
        print("socket binded to " + str(port))
        # listen on socket
        s.listen(5)

        c, addr = s.accept()
        print ("Got connection from " + str(addr))

        while True:

    	    # Establish connection with client
            data = c.recv(496)#.decode('utf-8')
            if not data: break

            #print("Client sent: ", str(input))
            # echo 8 bit number
            c.send(data)#.encode(decode('utf-8')))

        #-----------------------------------------------
        c.close() #close connection with client
        s.close() #close socket
        #-----------------------------------------------


if __name__ == '__main__':
	  main()
