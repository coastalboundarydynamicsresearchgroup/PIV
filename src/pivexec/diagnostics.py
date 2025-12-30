import os
#import shutil
#import math
import time
import json
import requests

dataPathRoot = '/pivdata/data/'


class Diagnostics:
    pivFilePath = dataPathRoot + '/default'
    logFile = pivFilePath + 'default.log'
    run_started = False
    logfile_cache = []

    runstate = {}
    baseBackendUrl = ''

    def __init__(self):
        configuration = {}
        with open('../configuration/configuration.json') as f:
            configuration = json.load(f)
        Diagnostics.baseBackendUrl = 'http://' + configuration['services']['backend']['host'] + ':' + configuration['services']['backend']['port']

    def start_new_run(self, runstate, pivFilePath):
        Diagnostics.runstate = runstate

        Diagnostics.logFile = os.path.join(pivFilePath, "piv.log")
        if not runstate.is_test() or runstate.get_testScanNumber() == 0:
            with open(Diagnostics.logFile, "w") as outfile:
                outfile.write('Start of log file ' + Diagnostics.logFile + '\n')

        Diagnostics.run_started = True

    def emit_status(self, message, logToFile=True, logToProgress=False, options=None):
        if logToProgress:
            payload = {}
            if options:
                payload = options

            if message and len(message) > 0:
                status = message.replace('"', '\\\"')
                payload['status'] = status

            requests.put(Diagnostics.baseBackendUrl + '/piv/progress/deploy', json=payload)

        if message and len(message) > 0:
            utcDateTime = time.gmtime()
            timestamp = "{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}".format(year=utcDateTime.tm_year, month=utcDateTime.tm_mon, day=utcDateTime.tm_mday, hour=utcDateTime.tm_hour, minute=utcDateTime.tm_min, second=utcDateTime.tm_sec)

            if logToFile:
                print(timestamp + ': ' + message)

                if not Diagnostics.run_started:
                    Diagnostics.logfile_cache.append(timestamp + ': ' + message + '\n')
                else:
                    with open(Diagnostics.logFile, "a") as outfile:
                        for log in Diagnostics.logfile_cache:
                            outfile.write(log)
                        Diagnostics.logfile_cache = []

                        outfile.write(timestamp + ': ' + message + '\n')

class DiagnosticSingleton:
  instance = None

  def __init__(self):
    raise Error('Use DiagnosticSingleton.getInstance()')
  
  def get_instance():
    if (not DiagnosticSingleton.instance):
      DiagnosticSingleton.instance = Diagnostics()

    return DiagnosticSingleton.instance

