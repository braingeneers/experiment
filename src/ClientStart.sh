#!/bin/bash
#Client Configuration

PORT='5003'
MASTER_HOSTNAME='localhost'

#start program
python3 client.py $MASTER_HOSTNAME $PORT
