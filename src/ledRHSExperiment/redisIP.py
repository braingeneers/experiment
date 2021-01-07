import redis
import os
import socket

def get_pi_name(filename):
    with open(filename) as f:
        return f.read()

with open(os.path.expanduser('~pi/.redis/credentials')) as f:
	redis_password = f.read().strip()
	redis_client = redis.Redis(host='67.58.49.54', port=6379, password=redis_password)
	gw = os.popen("ip -4 route show default").read().split()
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect((gw[2], 0))
	ip = s.getsockname()[0]
	gateway = gw[2]
	host = socket.gethostname()
	#print ("IP:", ip, " GW:", gateway, " Host:", host)
	#print(host) 
	#print(ip)
	redis_client.mset({host: ip})

