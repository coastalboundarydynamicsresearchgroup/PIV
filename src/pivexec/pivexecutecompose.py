import os
import shutil
import time
import math
import json
import requests

configurationpath = '/pivdata/configuration/'
dataPathRoot = '/pivdata/data/'

result = { 'success': False, 'message': 'Unknown error' }


class PivExecuteCompose:
    pivFilePath = dataPathRoot + '/default'

    logFile = pivFilePath + 'default.log'
    baseBackendUrl = ''

    def __init__(self, runstate):
        global dataPathRoot

        self.dataPath = dataPathRoot
        
        configuration = {}
        with open('../configuration/configuration.json') as f:
            configuration = json.load(f)
        PivExecuteCompose.baseBackendUrl = 'http://' + configuration['services']['backend']['host'] + ':' + configuration['services']['backend']['port']

        self.runstate = runstate

        if self.runstate.test:
            self.dataPath = dataPathRoot + 'test/'

            # All subsequent test scans will go in the test folder, start fresh for the first one.
            if self.runstate.get_testScanNumber() == 0:
                shutil.rmtree(self.dataPath, ignore_errors=True)

            os.makedirs(self.dataPath, exist_ok=True)

        self.pivFilePath = dataPathRoot + 'default/'


        self.makeNewDataFolder()

        self.runstate.get_configuration()['name'] = self.runstate.get_configurationName()
        config = json.dumps(self.runstate.get_configuration(), indent=4)

        with open(self.pivFilePath + "configuration.json", "w") as outfile:
            outfile.write(config)

        with open(self.pivFilePath + "RunIndex.csv", "w") as outfile:
            outfile.write("Time Stamp,Type,File\n")

    def emit_status(self, message, logToFile=True, logToProgress=False, options=None):
        if logToProgress:
            payload = {}
            if options:
                payload = options

            if message and len(message) > 0:
                status = message.replace('"', '\\\"')
                payload['status'] = status

            requests.put(PivExecuteCompose.baseBackendUrl + '/piv/progress/deploy', json=payload)

        if message and len(message) > 0:
            utcDateTime = time.gmtime()
            timestamp = "{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}".format(year=utcDateTime.tm_year, month=utcDateTime.tm_mon, day=utcDateTime.tm_mday, hour=utcDateTime.tm_hour, minute=utcDateTime.tm_min, second=utcDateTime.tm_sec)

            if logToFile:
                if self.runstate.test:
                    print(timestamp + ': ' + message)

                with open(logFile, "a") as outfile:
                    outfile.write(timestamp + ': ' + message + '\n')


    def stop_deployment(self):
        self.emit_status("Stopping deployment", logToFile=False, logToProgress=True, options={'deploying':False,'deployrunning':False})
        requests.put(PivExecuteCompose.baseBackendUrl + '/piv/stop')
        self.runstate.running = False


    def makeNewDataFolder(self):
        global pivFilePath
        global logFile

        utcDateTime = time.gmtime()
        data_folder = "{year:04d}-{month:02d}-{day:02d}_{hour:02d}.{minute:02d}.{second:02d}".format(year=utcDateTime.tm_year, month=utcDateTime.tm_mon, day=utcDateTime.tm_mday, hour=utcDateTime.tm_hour, minute=utcDateTime.tm_min, second=utcDateTime.tm_sec)
        self.pivFilePath = self.dataPath + data_folder + '/'

        if not os.path.exists(self.pivFilePath):
            os.makedirs(self.pivFilePath)

        logFile = self.pivFilePath + "piv.log"
        with open(logFile, "w") as outfile:
            outfile.write('Start of log file ' + logFile + '\n')

