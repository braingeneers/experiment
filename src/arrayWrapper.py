#!/usr/bin/python
#usage python3 organoidWrapper.py 5001

#=====USAGE========================
# To run code locally:
# usage: python3 organoidWrapper.py runlocal
# Otherwise request defaults to run through AWS
#===================================

import numpy as np
import time
#import matplotlib.pyplot as plt

import sys
import os
import os.path
#import PIL
import boto3
import json
#from PIL import Image
#-----------------------------------------------
import socket
import random
#from protocol import Message

#Real or Simulation experiment?
#import array
#from array import ArrayReal
#Usage: python3 organoidWrapper.py host port

from picamera import PiCamera
from time import sleep

#!/usr/bin/python

import wiringpi
import numpy as np

from picamera import PiCamera
from time import sleep

SDI = 27 #16 #//27   //serial data input
RCLK =  29 #21 //28   //memory clock input(STCP)
SRCLK =  28  #20 //29   //shift register clock input(SHCP)

SDI_2  = 27 #13 //27   //serial data input
RCLK_2  = 28 #19 //28   //memory clock input(STCP)
SRCLK_2 = 29 #26 //29   //shift register clock input(SHCP)

#LED Indication
IND_SERVER_CONNECTION = 0  #17
IND_SERVER_MSG_RCV = 7    #4
IND_CLIENT_POWER = 9      #3
IND_CLIENT_MSG_SEND = 8    #2

#unsigned char LED[8] = {0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80};

ARRAY_SIZE = 8 #leds per array

pins = [SDI, RCLK, SRCLK, SDI_2, RCLK_2, SRCLK_2, IND_SERVER_CONNECTION, IND_SERVER_MSG_RCV, IND_CLIENT_POWER, IND_CLIENT_MSG_SEND]
indPins = [IND_SERVER_CONNECTION, IND_SERVER_MSG_RCV, IND_CLIENT_POWER, IND_CLIENT_MSG_SEND]
LED_MASK = 128 #0x80
#define STANDARD_DELAY 25 //ms
#define LONG_DELAY 1000 //ms

#    wiringpi.pinMode(IND_SERVER_CONNECTION, 1)       # Set pin 6 to 1 ( OUTPUT )
#    wiringpi.digitalWrite(IND_SERVER_CONNECTION, 1)  # Write 1 ( HIGH ) to pin 6
#    wiringpi.shiftOut(1, 2, 0, 123)  # Shift out 123 (b1110110, byte 0-255) to data pin 1, clock pin 2


class ArrayReal:

    def __init__(self, sdi, rclk, srclk):
        print("Initializing Array!!")
        self.sdi = sdi
        self.rclk = rclk
        self.srclk = srclk

    def shiftin(self, patternString, pattern):
        for i in range(ARRAY_SIZE):
            pattern[i] = (patternString & (LED_MASK >> i)) > 0


    def pulse(self, pin):
        wiringpi.digitalWrite(pin, wiringpi.GPIO.LOW)
        wiringpi.digitalWrite(pin, wiringpi.GPIO.HIGH)


    def activate(self, pattern): #        void activate(int sdi, int rclk, int srclk, bool * pattern){
        print("Set array by shiftin()")
        for i in range(ARRAY_SIZE):
            out = (pattern & (LED_MASK >> i)) > 0
            print("out: ", out)
            wiringpi.digitalWrite(self.sdi, (out))
            self.pulse(self.srclk);
        self.pulse(self.rclk)


    def initPins(self): #set  pins as outputs

        wiringpi.wiringPiSetup()
        #initialize all pins to be outputs, initially low
        for pin in pins:
            wiringpi.pinMode(pin, wiringpi.GPIO.OUTPUT)
            wiringpi.digitalWrite(pin, wiringpi.GPIO.LOW)

    	#flash indication leds to ensure they work
        for indPin in indPins:
            wiringpi.digitalWrite(indPin, wiringpi.GPIO.HIGH)

    	#delay(LONG_DELAY)
        wiringpi.delay(1000)
        for indPin in indPins:
            wiringpi.digitalWrite(indPin, wiringpi.GPIO.LOW)

    	#turn power indication LED on
        wiringpi.digitalWrite(IND_CLIENT_POWER, wiringpi.GPIO.HIGH)


    def shutDownPins(self):
        for pin in pins:
            wiringpi.digitalWrite(pin, wiringpi.GPIO.LOW)
        self.activate(0)

    def statusConnected(self):
        wiringpi.digitalWrite(IND_SERVER_CONNECTION, wiringpi.GPIO.HIGH)

    def statusPreSendMsg(self):
         wiringpi.digitalWrite(IND_CLIENT_MSG_SEND, wiringpi.GPIO.HIGH)

    def statusSentMsg(self):
         wiringpi.digitalWrite(IND_CLIENT_MSG_SEND, wiringpi.GPIO.LOW)

    def statusAwaitingMsg(self):
         wiringpi.digitalWrite(IND_SERVER_MSG_RCV, wiringpi.GPIO.LOW)

    def statusRecievedMsg(self):
         wiringpi.digitalWrite(IND_SERVER_MSG_RCV, wiringpi.GPIO.HIGH)

def plot_stim(name, seq_num, pattern, num_inputs):
    plt.figure()
    theta = np.linspace(0, 2*np.pi, 9)[:-1]
    points = 25*np.array((np.cos(theta), np.sin(theta))) + 35
    #print("Theta: " + str(theta))
    #print("Points: "+ str(points[1][1]))
    plt.xlim(-3.4, 73.4)
    plt.ylim(-3.4, 73.4)
    x = points[0,:]
    y = points[1,:]
    bins = np.array([bit=='1' for bit in np.binary_repr(pattern, width=8)])
    #print(bins)
    index = []
    for j in range(0,8):
        if(not bins[j]):
            #print("i is: " + str(bins[i]))
            index.append(j)
    x = np.delete(x, index)
    y = np.delete(y, index)
    plt.plot(x,y, 'o', color='tab:orange')
    plt.savefig(name + str(seq_num) + '_' + str(np.binary_repr(pattern, width=num_inputs))+'_'+'stim'+'.png')
    plt.close('all')


def makeVideo():
    os.system("ffmpeg -r 3 -i figures/out/img%d.png -vcodec mpeg4 -y figures/movie.mp4")


def configuredExperiment(inputArray, filepath):
        #Iniialize Organoid
        myArray = ArrayReal(SDI, RCLK, SRCLK)
        myArray.initPins()
        seq_num = 0 #feedback loop sequence number

        for input in inputArray:
            print("Input: ", input)
            pattern = int(input[0])
            duration = int(input[1]*100)
            print("Pattern ", seq_num, ": ", pattern)

            #Organoid Simulation
            myArray.activate(pattern)
            wiringpi.delay(duration)

            #sim.make_rob_a_picture(filepath+"out/", seq_num, 1000, 1100, pattern)
            #camera = PiCamera()
#            plot_stim(filepath+"stim/", seq_num, pattern=pattern, num_inputs=ARRAY_SIZE)

            seq_num+=1 #increment sequence number

        #makeVideo()
        myArray.shutDownPins()
        return


def main():
        #if no ~/<GUID>.txt, generate guid
        #...
        #if no <GUID>queue on sqs, generate queue
        #...
        filepath = 'figures/'
        if (len(sys.argv) > 1 and sys.argv[1] == "runlocal"):
            print("Running Local!")
            f = "ec5600d8-17b5-45e5-93d6-2895119cb341.npy"
            inputArray = np.load(f)
            print(inputArray)
            configuredExperiment(inputArray, filepath)
            print("Done!")
            with open(e_guid + ".json", 'w') as fp:
                json.dump(data, fp)
        else:
            sqs = boto3.client('sqs')
            s3 = boto3.client('s3')

            #share current IP address info (for debugging through ssh when screenless/keyboardless)
            ses = boto3.client('ses')
            email_from = email_to= 'kvoitiuk@ucsc.edu'
            emaiL_subject = 'Raspberry Pi is Online'
            current_ip = str(socket.gethostbyname(socket.gethostname()))
            email_body = current_ip

            response = ses.send_email(
                Source = email_from,
                Destination={
                    'ToAddresses': [
                        email_to,
                    ]
                },
                Message={
                    'Subject': {
                        'Data': emaiL_subject
                    },
                    'Body': {
                        'Text': {
                            'Data': email_body
                        }
                    }
                }
            )


            source_bucket = 'braingeneers-receiving'
            dest_bucket = 'braingeneers-providing'

            #find virtualExperimentQueues
            queues = sqs.list_queues(QueueNamePrefix='realExperimentQueue') # we filter to narrow down the list
            queue_url = queues['QueueUrls'][0]
            print(queue_url)

            while True:
                print("Getting message from sqs")
                # Get experiment request from queue
                messages = sqs.receive_message(QueueUrl=queue_url,MaxNumberOfMessages=1, WaitTimeSeconds=20) # adjust MaxNumberOfMessages if needed
                if 'Messages' in messages: # when the queue is exhausted response dict contains no 'Messages' key
                        message = messages['Messages'][0] # 'Messages' is a list
                        # process the messages
                        guid = message['Body']
                        print("Experiment guid:", guid)

                        #Get the experiment instructions json in s3
                        key_json = guid + ".json"
                        f = s3.get_object(Bucket=source_bucket, Key=key_json)
                        file_content = f['Body'].read().decode('utf-8')
                        data = json.loads(file_content)
                        #data = json.loads(f['Body'])#json.loads(f['Body'])
                        print(data)
                        # Read json values
                        experiment = data["experiment"]
                        print(experiment)

                        # Delete the message from queue
                        sqs.delete_message(QueueUrl=queue_url,ReceiptHandle=message['ReceiptHandle'])

                        # Experiment configured or dynamic?
                        if(experiment["input"] == "configured"):
                            key_npy = guid + ".npy"
                            print("Key:", key_npy)
                            f = guid + ".npy"
                            print("Local Filename:", f)
                            s3.download_file(source_bucket, key_npy, f)
                            print("Downloaded!")
                            inputArray = np.load(f)
                            print(inputArray)
                            configuredExperiment(inputArray, filepath)

                            #upload results to s3
                            path = os.getcwd() #get current working directory
                            for root,dirs,files in os.walk(path+"/figures"):
                                for file in files:
                                    s3.upload_file(os.path.join(root,file), dest_bucket, guid + "/" + "data" + "/" + file)

                            #Notify "Experiment Done" to AWS Lambda
                            done_queues = sqs.list_queues(QueueNamePrefix='requestCompleteQueue') # we filter to narrow down the list
                            done_queue_url = done_queues['QueueUrls'][0]
                            enqueue_response = sqs.send_message(QueueUrl=done_queue_url, MessageBody=guid)
                        else:
                            return

                else:
                    print("No requests, going to sleep...")
                    time.sleep(60)        #dynamicExperiment()



if __name__ == '__main__':
	  main()
