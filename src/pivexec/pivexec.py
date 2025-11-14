import sys
import time
import json

from filewatcher import Watcher
from hardwarecomm import HardwareCommChannel
from flirexecutecompose import FlirExecuteCompose
from picoexecutecompose import PicoExecuteCompose

configurationpath = '/piv/configuration/'


def ExecuteDeploy(runstate):
  """ Callback sent to the file watcher that allows
      the deployment to execute when a runfile is present.
  """
  connectionStyle = "flir"
  if 'ConnectionStyle' in runstate.configuration:
    connectionStyle = runstate.configuration['ConnectionStyle']

  if connectionStyle == "flir":
    deployer = FlirExecuteCompose(runstate)
    deployer.compose_and_execute()
  elif connectionStyle == "pico":
    deployer = PicoExecuteCompose(runstate)
    deployer.compose_and_execute()
  else:
    print("Unknown connection style: " + connectionStyle)
    return


"""
    Backend implementation for sonar881 controller.
    Start the deployment engine.
"""
debug = False
if len(sys.argv) > 1:
  debug = True

watcher = Watcher(ExecuteDeploy, debug)
watcher.run()

exit(0)
