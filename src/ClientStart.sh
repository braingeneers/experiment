#!/bin/bash
#Client Configuration

PORT='5003'
MASTER_IP='localhost'

#start program
python3 client.py $MASTER_IP $PORT
