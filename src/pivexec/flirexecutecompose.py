import os
import time
import math
import json
import requests
from camera import Camera

from pivexecutecompose import PivExecuteCompose

result = { 'success': False, 'message': 'Unknown error' }


class FlirExecuteCompose(PivExecuteCompose):
  samplePeriod = 0.1   # Status reads in seconds

  def __init__(self, runstate):
    super().__init__(runstate)


  def delay_start(self):
    delay_minutes = float(self.runstate.configuration['Minutes'])
    delay_seconds = int(delay_minutes * 60)

    self.emit_status('Waiting for ' + str(delay_seconds) + ' seconds', logToProgress=True, options={'deployrunning':True})
    for second in range(delay_seconds):
      self.emit_status('Startup delay', logToFile=False, logToProgress=True, options={'delaySec':delay_seconds - second})
      time.sleep(1)
      if not self.runstate.is_running():
        break
    self.emit_status('Done waiting ' + str(delay_seconds) + ' seconds', logToProgress=True, options={'delaySec':0})


  def camera_configure(self, camera):
    # Configure the camera with the settings from the configuration
    # TODO - Add new methods to the Camera class in order to set up additional camera capabilities.
    camera.configure_trigger()
    camera.configure_exposure(self.runstate.configuration['ShutterOpenTime'])
    camera.configure_black_level(self.runstate.configuration['CameraBlacklevel'])
    camera.configure_gain(self.runstate.configuration['CameraGain'])
    camera.configure_gamma(self.runstate.configuration['CameraGamma'])

  def camera_reset_configuration(self, camera):
    # Reset the camera configuration to default
    # TODO - Add new methods as needed to return the camera to a default state.
    camera.reset_trigger()
    camera.reset_exposure()
    camera.reset_black_level()
    camera.reset_gain()
    camera.reset_gamma()

  def compose_and_execute(self):
    with Camera() as camera:
      if not camera.valid:
        self.emit_status(camera.status, logToFile=False, logToProgress=True, options={'deploying':False,'deployrunning':False})
        return
      
      self.delay_start()

      # TODO - additional camera setup may be in camera_configure, or new code may be added here.
      self.camera_configure(camera)
      camera.start_acquisition_mode()

      while self.runstate.is_running():
        start_timestamp = time.time()

        # TODO - Add code to trigger camrea/laser, if per-image-pair is needed.
        end_timestamp = time.time()
        duration = end_timestamp - start_timestamp
        while self.runstate.is_running() and duration < FlirExecuteCompose.samplePeriod:
          camera.acquire_image(self.pivFilePath)
          duration += 0.1

      camera.end_acquisition_mode()
      self.camera_reset_configuration(camera)
      self.emit_status("Compose and deploy '" + self.runstate.get_configurationName() + "' complete", logToFile=False, logToProgress=True, options={'deploying':False,'deployrunning':False})
