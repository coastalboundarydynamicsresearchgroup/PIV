import picamera
from datetime import datetime
import time

# Set the working directory
WORKING_DIR = "/home/pi/osutech"
# Define the desired resolutions (width, height)
RESOLUTIONS = [(880, 584), (1010, 672), (1240, 824), (1740, 1140)]
# Define the desired frame rates for each phase (frames per second)
FRAME_RATES = [120, 90, 60, 30]
# Duration of video annoatation(in seconds)
ANNOTATION_DURATION = 0.2  #annotation period 
# Duration of each individual video (in seconds)
VIDEO_DURATION = 10
# Function to turn on laser
def turn_on_laser():
    print("Turning on laser")
    # Add code here to turn on the laser
# Function to turn off laser
def turn_off_laser():
    print("Turning off laser")
    # Add code here to turn off the laser
# Function to record video with dynamic timestamp annotation
def record_video(resolution, frame_rate):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")  # Include microseconds
    filename = f"{WORKING_DIR}/video_{timestamp}.h264"
    print(f"Recording video: {filename}")
    with picamera.PiCamera() as camera:
        camera.resolution = resolution
        camera.framerate = frame_rate
        camera.start_preview()
        camera.start_recording(filename)
        start_time = time.time()
        while time.time() - start_time < VIDEO_DURATION:
            camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            camera.wait_recording(ANNOTATION_DURATION)
        camera.stop_recording()
    print("Recording complete")
# Main loop to record videos for each resolution and frame rate
tick = datetime.now() 
while True:
    for resolution, frame_rate in zip(RESOLUTIONS, FRAME_RATES):
          record_video(resolution, frame_rate)
    if (datetime.now() - tick).seconds > 50:
        print("Time has exceeded 50 seconds!")
        break



try:
    while True:
       for resolution, frame_rate in zip(RESOLUTIONS, FRAME_RATES):
          record_video(resolution, frame_rate)
except KeyboardInterrupt:
    camera.stop_preview() ## G - still no camera object?
    endstamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")
    print("Previewing stopped at:" endstamp)  







