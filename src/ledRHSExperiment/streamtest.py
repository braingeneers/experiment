#!/usr/bin/env python3 
import subprocess 
import picamera 
import time 
YOUTUBE="rtmp://a.rtmp.youtube.com/live2/" 
KEY= "85f6-v3xc-jtvs-stps-a2s6"
stream_cmd = 'ffmpeg -f h264 -r 25 -i - -itsoffset 5.5 -fflags nobuffer  -f alsa -ac 1 -vcodec copy  -acodec aac -ac 1 -i anullsrc  -ar 8000 -ab 32k -map 0:0 -map 1:0 -strict experimental -f flv ' + YOUTUBE + KEY 
stream = subprocess.Popen(stream_cmd, shell=True, stdin=subprocess.PIPE) 
camera = picamera.PiCamera(resolution=(640, 480), framerate=25) 
try: 
  now = time.strftime("%Y-%m-%d-%H:%M:%S") 
  camera.framerate = 25 
  camera.vflip = True 
  camera.hflip = True 
  camera.start_recording(stream.stdin, format='h264', bitrate = 2000000) 
  while True: 
     camera.wait_recording(1) 
except KeyboardInterrupt: 
     camera.stop_recording() 
finally: 
  camera.close() 
  stream.stdin.close() 
  stream.wait() 
  print("Camera safely shut down") 
  print("Good bye") 
