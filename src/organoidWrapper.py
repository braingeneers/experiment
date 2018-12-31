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

def main():

        print(("Arg1: %s Arg2: %s" % (sys.argv[1], sys.argv[2])))
        msg = Message.announce(sys.argv[2], sys.argv[1], socket.gethostname(), Message.PI, random.randint(0,5009))

#=====================Communicate with Client==========================
#Listen for Client



if __name__ == '__main__':
	  main()
