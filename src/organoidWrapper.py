#!/usr/bin/python
#usage python3 organoid.py 5001

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import time
#import drywetlab

import sys
import numpy
from PIL import Image


#-----------------------------------------------
import socket
import pickle
import random
from protocol import Message

def main():

        print(("Arg1: %s Arg2: %s" % (sys.argv[1], sys.argv[2])))

        s = socket.socket() #create socket
        port = int(sys.argv[2]) #bind to port

        # connect to server
        host_ip = socket.gethostbyname(str(sys.argv[1]))
        s.connect((host_ip, port))

        #Client data message to be sent to server
        msg = Message(who = Message.PI, host_ip=socket.gethostbyname(socket.gethostname()), port=random.randint(0,5009))
        #print(msg.who + msg.host_ip, msg.port)
        print(msg)
        #Pickle Message and send it to sever
        data_string = pickle.dumps(msg)
        s.send(data_string)


        out = s.recv(1024) # receive echo from client
        msg = pickle.loads(out)
        print("Recieved: ", str(msg))
        time.sleep(1)


        #-----------------------------------------------
        s.close() #close socket
        #-----------------------------------------------



if __name__ == '__main__':
	  main()
