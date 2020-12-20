import board
import neopixel
import redis
import time
import os

pixels = neopixel.NeoPixel(board.D18, 1, brightness=0.5, pixel_order=neopixel.GRB)
wait = 0.25

with open(os.path.expanduser('~pi/.redis/credentials')) as f:
	redis_password = f.read().strip()
	redis_client = redis.Redis(host='67.58.49.54', port=6379, password=redis_password)
	while True:
		red  = int(redis_client.get("Red"))
		green = int(redis_client.get("Green"))
		blue = int(redis_client.get("Blue"))
		print(red, green, blue)
		pixels[0] = (red, green, blue)
		time.sleep(wait)


