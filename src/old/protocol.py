#!/usr/bin/python
import socket, pickle


class Message:
    CLIENT = 0
    PI = 1
    MASTER = 2

    def __init__(self, who, host_ip, port, num_organoids, id = None, success = None):
        self.who = who #e.g. client
        self.host_ip = host_ip #this machine's ip
        self.port = port #this machine's specified  port
        self.id = id
        self.num_organoids = num_organoids
        self.success = success

    def __str__(self):
        return "MESSAGE   Who: %s   IP: %s    Port: %d    Id:%s     Success: %s" % \
                (self.stringifyWho(), \
                 self.host_ip, self.port, \
                 ("None" if (self.id == None) else str(self.id)), \
                 ("False" if (self.success == None) else "True"))


    def stringifyWho(self):
        if (self.who == Message.CLIENT):
            return "Client"
        elif (self.who == Message.PI):
            return "Pi"
        return "Master"


    """
    class Experiment:
        def __init__():
            self.numOrganoids = 0
            self.
    """
