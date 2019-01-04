#!/usr/bin/python
#usage python3 organoidWrapper.py 5001

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
#Usage: python3 organoidWrapper.py host port

class RasPi:
    server_hostname = None
    server_port = None
    num_organoids = None
    my_hostname = None
    my_ip_address = None
    my_port = None
    my_id = None

    def __init__(self, master_hostname, master_port, num_organoids):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket
        self.port = int(master_port)
        # connect to server
        host_ip = socket.gethostbyname((master_hostname))
        self.s.connect((host_ip, self.port))
        print("connected to " + master_hostname)
        RasPi.num_organoids=int(num_organoids)
        RasPi.my_hostname = socket.gethostname()
        RasPi.my_ip_address = socket.gethostbyname(RasPi.my_hostname)
        RasPi.my_port= RasPi.server_port = self.port #can use same port number on RasPi as on Master
        RasPi.my_id=None
        RasPi.server_hostname=master_hostname



    def checkIP(self):
        currentIP = socket.gethostbyname(socket.gethostname())
        if(currentIP != RasPi.my_ip_address):
             sendMsg(RasPi.server_port, RasPi.server_hostname, socket.gethostname(), \
                        Message.PI, RasPi.my_port, RasPi.my_id)

    def sendMsg(self):
        #Client data message to be sent to server
        msg = Message(Message.PI, socket.gethostbyname(str(RasPi.my_hostname)), \
                        RasPi.my_port, RasPi.num_organoids, RasPi.my_id, False)
            	#print(msg.who + msg.host_ip, msg.port)
        print(msg)
        #Pickle Message and send it to sever
        data_string = pickle.dumps(msg)
        self.s.send(data_string)
        #time.sleep(1)

    def receiveMsg(self):
        out = self.s.recv(2048) # receive echo from client
        msg = pickle.loads(out)
        print("Recieved: ", str(msg))
        self.s.close()
        return msg

    def closeService(self):
        self.s.close() #close socket

def main():

        print(("Arg1: %s Arg2: %s" % (sys.argv[1], sys.argv[2])))
        Pi = RasPi(sys.argv[1], sys.argv[2], sys.argv[3])
        Pi.sendMsg()
        #msg = Pi.receiveMsg()
        #print("My ID is:", msg.id)


        #========================Experiment==========================
        while(True):
            time.sleep(3500) #5min
            #Pi.checkIP()



        Pi.closeService()


if __name__ == '__main__':
	  main()
