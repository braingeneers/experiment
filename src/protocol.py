#!/usr/bin/python
import socket, pickle


class Message:
    CLIENT = 0
    PI = 1
    MASTER = 2

    def __init__(self, who, host_ip, port, success = 'None'):
        self.who = who #client
        self.host_ip = host_ip
        self.port = port
        self.success = success

    def __str__(self):
        return "MESSAGE   Who: %s   IP: %s    Port: %d" % \
                (("Client" if (self.who == Message.CLIENT) else "Pi"), \
                 self.host_ip, self.port)
        #return "Messae prined!"

    def announce(server_port, server_hostname, my_hostname, role, my_newPort):
        s = socket.socket() #create socket
        port = int(server_port) #bind to port

        # connect to server
        host_ip = socket.gethostbyname((server_hostname))
        s.connect((host_ip, port))

        #Client data message to be sent to server
        msg = Message(who = role, host_ip=socket.gethostbyname(my_hostname), port=my_newPort)
            	#print(msg.who + msg.host_ip, msg.port)
        print(msg)
        #Pickle Message and send it to sever
        data_string = pickle.dumps(msg)
        s.send(data_string)

        out = s.recv(2048) # receive echo from client
        msg = pickle.loads(out)
        print("Recieved: ", str(msg))
        s.close()
        return msg


    """
    class Experiment:
        def __init__():
            self.numOrganoids = 0
            self.
    """
