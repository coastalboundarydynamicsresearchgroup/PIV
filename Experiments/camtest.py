from picamera import PiCamera
from time import sleep
from subprocess import call


camera = PiCamera()
camera.resolution = (1012,760)
camera.framerate = 120
camera.start_preview()
camera.start_recording('/home/pi/Desktop/videotest.h264')
sleep(10)
camera.stop_recording()
camera.stop_preview()
command = "MP4Box -add /home/pi/Desktop/videotest.h264 /home/pi/Desktop/convertedVideo.mp4"
# Execute our command
call([command], shell=True)