#! /bin/bash  --- edit this 

import os                   
import subprocess           
import numpy as np
from time import sleep
from datetime import datetime
import RPi.GPIO as GPIO    
import picamera 


# Set the working directory
WORKING_DIR = "/home/pi/osutech"
# Set desired frame rate and resolution
FRAME_RATE = 30  # in frames per second
RESOLUTION = (1280, 720)  # width, height
# Function to record video with timestamp
def record_video():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")  # Include microseconds
    filename = f"{WORKING_DIR}/video_{timestamp}.h264"
    mp4_filename = f"{WORKING_DIR}/video_{timestamp}.mp4"
    print(f"Recording video: {filename}")
    with picamera.PiCamera() as camera:
        camera.resolution = RESOLUTION
        camera.framerate = FRAME_RATE
        camera.start_recording(filename)
        start = datetime.now()
        while (datetime.now() - start).seconds < 10:   #records 10 seconds 
            camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            camera.wait_recording(0.2)      #amount of time before it annotates the screen again
        camera.stop_recording()
    print(f"Video recorded: {filename}")
    # Convert to MP4
    #print("Converting to MP4...")
    #with open(filename, "rb") as h264file, open(mp4_filename, "wb") as mp4file:
     #   mp4file.write(h264file.read())
    #print(f"Video converted to MP4: {mp4_filename}")
# Main loop to continuously record every 5 minutes
tick = datetime.now() 
while True:
    record_video() #recording continuously
    # Wait for 5 minutes before recording the next video
    # time.sleep(300)
    if (datetime.now() - tick).seconds > 30:
        break
        print("Time has exceeded 30 seconds!")











