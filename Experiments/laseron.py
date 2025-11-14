import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
import datetime as dt
import os
import subprocess
import numpy as np


#setting up the green laser 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)
pinnumber = 12
GPIO.setup(pinnumber,GPIO.OUT)

def button(logiclevel):      #pin16 for now, only logic levels acceptable are 0 and 1 
    if logiclevel==1:   
        return GPIO.output(pinnumber,logiclevel)  
    if logiclevel==0:                                   ## G - Redundant if statement
        return GPIO.output(pinnumber,logiclevel)
    
def laser_on(): 
    button(0)
    sleep(0.25)         ## G - time.sleep() is notoriously inconsistent
    button(1)
    return "laser is on"

def laser_off():
    sleep(0.25)
    button(0)
    return "laser is on"  ## G - off?

laser_on()
sleep(10)
laser_off()
GPIO.cleanup()



