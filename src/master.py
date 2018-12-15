#!/usr/bin/python
#usage python3 organoid.py 5001

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
        print("Pis Ready: ", len(readyPi))
        for pi in readyPi:
            print(pi)
        print("Pis Busy:", len(busyPi))
        for pi in busyPi:
            print(pi)


    def controlFlow(self):
        # listen on socket
        s = self.s
        readyPi = Master.readyPi
        busyPi = Master.busyPi
        s.listen(5)
        while True:
            # Establish connection with client
            c, addr = s.accept()
            print ("Got connection from " + str(addr))

            # receive 8 bit number from client
            data_string = c.recv(2048)
            msg = pickle.loads(data_string)

            if (msg.who == Message.PI):
                readyPi.append(msg)
                replymsg = copy.deepcopy(msg)
                replymsg.who = Message.MASTER
                replymsg.success = True
                msg.success = True
                self.printPis()
                data_string = pickle.dumps(replymsg)
                print("Master sent: ", str(replymsg))
                c.send(data_string)
            elif (msg.who == Message.CLIENT):
                allocatedPi = copy.deepcopy(readyPi[0])
                busyPi.append(allocatedPi)
                data_string = pickle.dumps(allocatedPi)
                c.send(data_string)
                readyPi.pop(0)
                print("Pis Recorded: ", len(readyPi))
                for pi in readyPi:
                    print(pi)



    	#-----------------------------------------------
        c.close() #close connection with client
        s.close() #close socket
    	#-----------------------------------------------





def main():

    print("Arg1:" + sys.argv[1])

    #Init Master
    master = Master(sys.argv[1])

    #Manage resources/connections between Pi's and Clients
    master.controlFlow()



if __name__ == '__main__':
	  main()
