import sys
import time
import json

from filewatcher import Watcher
from hardwarecomm import HardwareCommChannel
from picoexecutecompose import PicoExecuteCompose

configurationpath = '/pivdata/configuration/'


def ExecuteDeploy(runstate):
  """ Callback sent to the file watcher that allows
      the deployment to execute when a runfile is present.
  """
  deployer = PicoExecuteCompose(runstate)
  deployer.compose_and_execute()


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
