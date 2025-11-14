import os
import RPi.GPIO as GPIO
from time import sleep

def lasertimeon(freq,dc):
    t = (dc/100)*((1/freq)*1000)
    print("time on for laser is:", t , "ms" )
    return t

def laser_pulse(freq, time_on):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(True)
    GPIO.setup(18,GPIO.OUT)
    pwm = GPIO.PWM(18,freq)
    pwm.start(0)
    duty_cycle = 100 * time_on / ((1/freq)*1000) #time_on has to be in milliseconds and f has to be in Hz
    pwm.ChangeDutyCycle(duty_cycle)
    sleep(10)
    pwm.stop()
    GPIO.cleanup()
    print("laser pulse complete at:", freq, "Hz and", duty_cycle,"% duty cycle")

f = 168
laseron = lasertimeon(f,50)
laser_pulse(f,laseron)