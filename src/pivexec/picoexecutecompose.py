import os
import time
import math
import json
import requests
from hardwarecomm import HardwareCommChannel
from camera import Camera

from pivexecutecompose import PivExecuteCompose

result = { 'success': False, 'message': 'Unknown error' }


class PicoExecuteCompose(PivExecuteCompose):
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


  def transact_pico(self, picocc, command):
    # Send command to the Pico
    picocc.sendCommand(command)

    # Wait for a response
    response = picocc.receiveCommand()

    # Parse the response
    try:
      result = json.loads(response)
    except json.JSONDecodeError as e:
      raise Exception("Invalid JSON response from Pico: " + str(e))

    return result

  def pico_send_configuration(self, picocc):
    configuration = self.runstate.configuration
    configuration['Command'] = 'Configure'
    if 'Debug' in configuration and configuration['Debug']:
       configuration["DebugMultiplier"] = 1000
    result = self.transact_pico(picocc, configuration)
    self.emit_status('Pico configuration sent', logToProgress=True, options={'deployrunning':True})
    return result
  
  def pico_send_command(self, picocc, command):
    """ For parameterless commands, send the command to the Pico
    and wait for a response. 
    Commands:
      'GetConfiguration'
      'Start'
      'Stop'
      'GetStatus'
    """
    commandObject = {'Command': command}
    result = self.transact_pico(picocc, commandObject)
    self.emit_status(f'Pico command {command} sent', logToProgress=True, options={'deployrunning':True})
    return result

  def camera_configure(self, camera):
    # Configure the camera with the settings from the configuration
    camera.configure_trigger()
    camera.configure_exposure(self.runstate.configuration['ShutterOpenTime'])
    camera.configure_black_level(self.runstate.configuration['CameraBlacklevel'])
    camera.configure_gain(self.runstate.configuration['CameraGain'])
    camera.configure_gamma(self.runstate.configuration['CameraGamma'])

  def camera_reset_configuration(self, camera):
    # Reset the camera configuration to default
    camera.reset_trigger()
    camera.reset_exposure()
    camera.reset_black_level()
    camera.reset_gain()
    camera.reset_gamma()

  def compose_and_execute(self):
    with HardwareCommChannel(self.runstate) as picocc:
      self.emit_status("Connecting to camera and acquiring info", logToFile=False, logToProgress=True, options={'deployrunning':True, 'count':0})
      with Camera() as camera:
        if not camera.valid:
          self.emit_status(camera.status, logToFile=False, logToProgress=True, options={'deploying':False,'deployrunning':False})
          return
        
        self.delay_start()

        self.pico_send_configuration(picocc)
        self.camera_configure(camera)
        camera.start_acquisition_mode()

        with open(self.pivFilePath + "RunSettings.json", "w") as outfile:
          runsettings = {}
          runsettings['pico'] = self.pico_send_command(picocc, 'GetConfiguration')
          runsettings['camera'] = {
            'MaxWidth':camera.caminfo['MaxWidth'], 
            'MaxHeight':camera.caminfo['MaxHeight'],
            'Width':camera.caminfo['Width'], 
            'Height':camera.caminfo['Height']
            }
          outfile.write(json.dumps(runsettings, indent=4))

        self.pico_send_command(picocc, 'Start')
        
        while self.runstate.is_running():
          start_timestamp = time.time()

          status = self.pico_send_command(picocc, 'GetStatus')
          running = status['IsRunning'] == 1
          self.emit_status(f"Configuration '{self.runstate.configuration['Name']}' executing", logToProgress=True, options={'deploying':running, 'deployrunning':running, 'count':status['CycleCount']})
          end_timestamp = time.time()
          duration = end_timestamp - start_timestamp
          while self.runstate.is_running() and duration < PicoExecuteCompose.samplePeriod:
            #sleepTime = 0.1 if PicoExecuteCompose.samplePeriod - duration >= 0.1 else PicoExecuteCompose.samplePeriod - duration
            #time.sleep(sleepTime)
            camera.acquire_image(self.pivFilePath)
            duration += 0.1

            if status['IsRunning'] != 1:
              self.stop_deployment()

        self.pico_send_command(picocc, 'Stop')

        # Clean any remaining images out of the camera buffer.
        images_remain = True
        while images_remain:
          images_remain = camera.acquire_image(self.pivFilePath)

        camera.end_acquisition_mode()
        self.camera_reset_configuration(camera)

        self.emit_status("Compose and deploy '" + self.runstate.get_configurationName() + "' complete", logToFile=False, logToProgress=True, options={'deploying':False,'deployrunning':False})
