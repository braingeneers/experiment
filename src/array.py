#!/usr/bin/python

import wiringpi
import numpy as np

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


class Array():

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


def main():

    myArray = Array(SDI, RCLK, SRCLK)
    myArray.initPins()

    inputArray = np.array([[1, 1], [2, 1], [4, 1], [8, 1], [16, 1], [32, 1], [64, 1], [128, 1], [0, 1], [1, 1], [2, 1], [4, 1], [8, 1], [16, 1], [32, 1], [64, 1], [128, 1], [0, 1]])

    for input in inputArray:
        myArray.activate(int(input[0]))
        wiringpi.delay(int(input[1]*1000))

    myArray.shutDownPins()
    return




if __name__ == '__main__':
	  main()
