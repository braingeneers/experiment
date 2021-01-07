import redis
import socket

def get_pi_name(filename):
    with open(filename) as f:
        return f.read()

with open(os.path.expanduser('~pi/.redis/credentials')) as f:
	redis_password = f.read().strip()
	redis_client = redis.Redis(host='67.58.49.54', port=6379, password=redis_password)
	name  = os.path.expanduser("~") 
	ip = socket.gethostbyname(socket.gethostname()) 
	redis_client.mset({name: ip})

