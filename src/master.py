#!/usr/bin/python
#usage python3 master.py 5001

import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation
#import pandas as pd
import time
import copy
import sys
import numpy
#from PIL import Image
import pickle
import socket
from protocol import Message

class Master:
    #arrays tracking Rasperry Pi units
    readyPi = []
    busyPi = []

    def __init__(self, listen_port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket
        self.port = int(listen_port)
        self.s.bind(('', self.port)) #bind to port
        print("socket binded to " + str(self.port))

    def printPis(self):
        print("Pis Ready: ", len(Master.readyPi))
        for pi in Master.readyPi:
            print(pi)
        print("Pis Busy:", len(Master.busyPi))
        for pi in Master.busyPi:
            print(pi)



    def controlFlow(self):
        # listen on socket
        self.s.listen(5)

        while True:
            # Establish connection with client
            c, addr = self.s.accept()
            print ("Got connection from " + str(addr))

            # receive message from client
            data_string = c.recv(2048)
            msg = pickle.loads(data_string)

            if (msg.who == Message.PI):
                self.servicePi(msg, c)

            elif (msg.who == Message.CLIENT):
                self.serviceClient(msg, c)

    	#-----------------------------------------------
        c.close() #close connection with client
    	#-----------------------------------------------

    def servicePi(self, msg, c):
        msg.success = True
        if (msg.id == None):
            print("# Ready pi:", len(Master.readyPi), "# Busy pi:",  len(Master.busyPi))
            msg.id = len(Master.readyPi) + len(Master.busyPi) + 1
        Master.readyPi.append(msg) #start tracking this Pi

        self.printPis() #show all Pis

        #reply to Pi
        replymsg = copy.deepcopy(msg)
        self.reply(replymsg, c, True)


    def serviceClient(self, msg,c):
        #reply to Client
        if not Master.readyPi:
            self.reply(msg, c, False)
        else:
            allocatedPi = copy.deepcopy(Master.readyPi[0])
            self.reply(allocatedPi, c, True)
            #update Pi tracking
            Master.busyPi.append(allocatedPi)
            Master.readyPi.pop(0)

            self.printPis()

    def reply(self, replymsg, c, success):
        replymsg.who = Message.MASTER
        replymsg.success = success

        data_string = pickle.dumps(replymsg)
        print("Master sent: ", str(replymsg))
        c.send(data_string)

    def closeService(self):
        s.close() #close socket









def main():

    print("Arg1:" + sys.argv[1])

    #Init Master
    master = Master(sys.argv[1])

    #Manage resources/connections between Pi's and Clients
    master.controlFlow()



if __name__ == '__main__':
	  main()
