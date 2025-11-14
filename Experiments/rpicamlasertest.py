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
        

# Set the working directory
WORKING_DIR = "/home/pi/osutech"
# Set desired frame rate and resolution
FRAME_RATE = 30  # in frames per second
RESOLUTION = (1920, 1080)  # width, height
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
        while (datetime.now() - start).seconds < 60:   #records 60 seconds 
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
    laser_on()
    record_video() #recording continously
    laser_off()
    sleep(30)
    if (datetime.now() - tick).seconds > 300:
        break
        print("Time has exceeded 5 minutes!")


GPIO.cleanup()
#os.system('sudo shutdown -h now')   #shutting down raspberry pi 