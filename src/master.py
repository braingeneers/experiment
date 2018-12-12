#!/usr/bin/python
#usage python3 organoid.py 5001

import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation
#import pandas as pd
import time

import sys
import numpy
#from PIL import Image

import pickle

#-----------------------------------------------
import socket


from protocol import Message

def main():

    #array containing avaliable Rasperry Pi units
    rasPi = []

    print("Arg1:" + sys.argv[1])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket

    #host = socket.gethostname()
    port = int(sys.argv[1])
    s.bind(('', port)) #bind to port
    print("socket binded to " + str(port))

	# listen on socket
    s.listen(5)
    while True:
        # Establish connection with client
        c, addr = s.accept()
        print ("Got connection from " + str(addr))

        # receive 8 bit number from client
        data_string = c.recv(2048)
        msg = pickle.loads(data_string)

        if (msg.who == Message.PI):
            rasPi.append(msg)
            print("Pis Recorded: ", len(rasPi))
            for pi in rasPi:
                print(pi)
        elif (msg.who == Message.CLIENT):
            allocatedPi = rasPi[0]
            data_string = pickle.dumps(allocatedPi)
            c.send(data_string)
            rasPi.pop(0)
            print("Pis Recorded: ", len(rasPi))
            for pi in rasPi:
                print(pi)



        print("Master sent: ")
        #print(msg.who, msg.host_ip, msg.port)
        print(msg)
        c.send(data_string)

	#-----------------------------------------------
    c.close() #close connection with client
    s.close() #close socket
	#-----------------------------------------------


if __name__ == '__main__':
	  main()
