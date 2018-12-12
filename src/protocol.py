#!/usr/bin/python

class Message:
    def __init__(self):
    	self.who = 0 #client
    	self.host_ip = 0
    	self.port = 0
    def __str__(self):
        return "MESSAGE -- Who: %d IP: %d Port: %d" % (self.who, self.host_ip, self.port)
        #return "Messae prined!"

        
class ConnectionMsg:
        def __init__(self):
            self.who = 0;
