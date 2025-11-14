import picamera
from datetime import datetime
import time

FRAME_RATE = 30  # in frames per second
RESOLUTION = (1280, 720)  # width, height

def record_video():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")
    print("Starting at:" timestamp)
    with picamera.PiCamera() as camera:
        camera.resolution = RESOLUTION
        camera.framerate = FRAME_RATE
        camera.start_preview()
        camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        camera.wait_recording(0.2) 
        
try:
    while True:
        record_video()    
except KeyboardInterrupt:
    camera.stop_preview()   ## G - camera undefined? included in picamera??
    endstamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")
    print("Previewing stopped at:" endstamp) 