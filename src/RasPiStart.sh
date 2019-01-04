#!/bin/bash
#Raspberry Pi Configuration

PORT='5003'
MASTER_HOSTNAME='localhost'
NUM_ORGANOIDS='1'

#start program
python3 organoidWrapper.py $MASTER_HOSTNAME $PORT $NUM_ORGANOIDS
