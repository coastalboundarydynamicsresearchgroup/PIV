import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
import datetime as dt
import os
import subprocess
import numpy as np

os.system('sudo hwclock -s --hctosys')               #set system clock to rtc clock

camera = PiCamera(resolution=(2028, 1520), framerate=40)
camera.start_preview()
camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S-%f")
str_current_datetime = str(current_datetime)
videos = str_current_datetime+".h264"
camera.start_recording(videos)
start = dt.datetime.now()
while (dt.datetime.now() - start).seconds < 30:   #records 30 seconds 
    camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    camera.wait_recording(0.2)      #amount of time before it annotates the screen again
camera.stop_recording()

 
