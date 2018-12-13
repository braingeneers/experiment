#!/usr/bin/python

#=====
#usage: python3 client.py host port
#example: python3 client.py localhost 5001
#======

import sys
import socket
import pickle
#import numpy as np
import random
import time
#import protocol #defines internal Messaging format


from protocol import Message


def main():
	print(("Arg1: %s Arg2: %s" % (sys.argv[1], sys.argv[2])))

	#Ask Master server for a Pi
	Message.announce(sys.argv[2], sys.argv[1], socket.gethostname(), Message.CLIENT, 5001)

	#time.sleep(1)



if __name__ == '__main__':
	  main()
