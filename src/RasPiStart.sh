#!/bin/bash
#Raspberry Pi Configuration

PORT='5003'
MASTER_IP='localhost'

#start program
python3 organoidWrapper.py $MASTER_IP $PORT
