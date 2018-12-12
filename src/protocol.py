#!/usr/bin/python

class Message:
    CLIENT = 0
    PI = 1
    

    def __init__(self, who, host_ip, port):
    	self.who = who #client
    	self.host_ip = host_ip
    	self.port = port
    def __str__(self):
        return "MESSAGE   Who: %s   IP: %s    Port: %d" % \
                (("Client" if (self.who == Message.CLIENT) else "Pi"), \
                 self.host_ip, self.port)
        #return "Messae prined!"


class ConnectionMsg:
        def __init__(self):
            self.who = 0;
