
from time import sleep
from datetime import datetime 
import os  ## G - ??
from subprocess import call
import numpy as np ## G - ??
import math


def fan_angle(d,h):
    theta = math.atan(h/(2*d))
    return math.degrees(theta)

def height(d, angle):
    h = 2*d*math.tan(math.radians(angle))
    return h

y = fan_angle(19,19.5)
x = height(17,y)
print(x)


## G - Should be class functions
                                

