#!/usr/bin/python3

import RPi.GPIO as GPIO
import picamera
from time import sleep
from datetime import datetime
import os
from subprocess import call
import numpy as np

#setting up the laser
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)
pinnumber = 12
GPIO.setup(pinnumber,GPIO.OUT)

#os.system('sudo hwclock --hctosys')               #set system clock to rtc clock

def button(logiclevel):      #pin12 for now, only logic levels acceptable are 0 and 1
    if logiclevel==1:
        return GPIO.output(pinnumber,logiclevel)
    if logiclevel==0:
        return GPIO.output(pinnumber,logiclevel)

def laser_on():
    button(0)
    sleep(0.25)
    button(1)
    sleep(0.25)
    button(0)
    return "laser is on"

def laser_off():
    button(0)
    sleep(0.25)
    button(1)
    sleep(0.25)
    button(0)
    return "laser is off"


#Set the working directory
WORKING_DIR = "/home/pi/osutech"
#Set desired frame rate and resolution
RESOLUTIONS = [(880,584), (1011,672), (1240,824), (1740, 1140)]
FRAME_RATES = [120, 90, 60, 30]
#Set desired video seetings
ANNOTATION_DURATION = 0.1 #seconds
VIDEO_DURATION = 15 #seconds
# Function to record video with timestamp
def record_video(resolution,frame_rate):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")  # Include microseconds
    filename = f"{WORKING_DIR}/video_{timestamp}.h264"
    #mp4_filename = f"{WORKING_DIR}/video_{timestamp}.mp4"
    #print(f"Recording video: {filename}")
    with picamera.PiCamera() as camera:
        camera.resolution = resolution
        camera.framerate = frame_rate
        camera.start_recording(filename)
        start = datetime.now()
        while (datetime.now() - start).seconds < VIDEO_DURATION:   #records this amount of time
            camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            camera.wait_recording(ANNOTATION_DURATION)      #amount of time before it annotates the screen again
        camera.stop_recording()
    #print(f"Video recorded: {filename}")
    # Convert to MP4
    #print("Converting to MP4...")
    #with open(filename, "rb") as h264file, open(mp4_filename, "wb") as mp4file:
        #mp4file.write(h264file.read())
   #print(f"Video converted to MP4: {mp4_filename}")

tick = datetime.now()
time_limit = 90 #amount of time for recording
while True:
    for resolution, frame_rate in zip(RESOLUTIONS, FRAME_RATES):
        laser_on()
        record_video(resolution, frame_rate)
        laser_off()
        sleep(5)
    if (datetime.now() - tick).seconds > time_limit:
        break
       # print('Time has exceeded:' time_limit )

GPIO.cleanup()
#os.system('sudo shutdown -h now')   #shutting down raspberry pi
