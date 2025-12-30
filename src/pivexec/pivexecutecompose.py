import os
import shutil
import time
import math
import json
import requests

from diagnostics import DiagnosticSingleton

configurationpath = '/pivdata/configuration/'
dataPathRoot = '/pivdata/data/'

result = { 'success': False, 'message': 'Unknown error' }


class PivExecuteCompose:
    pivFilePath = dataPathRoot + '/default'

    diagnostic = DiagnosticSingleton.get_instance()
    baseBackendUrl = ''

    def __init__(self, runstate):
        global dataPathRoot

        self.dataPath = dataPathRoot
        
        configuration = {}
        with open('../configuration/configuration.json') as f:
            configuration = json.load(f)
        PivExecuteCompose.baseBackendUrl = 'http://' + configuration['services']['backend']['host'] + ':' + configuration['services']['backend']['port']

        self.runstate = runstate

        if self.runstate.is_test():
            self.dataPath = dataPathRoot + 'test/'

            # All subsequent test scans will go in the test folder, start fresh for the first one.
            if self.runstate.get_testScanNumber() == 0:
                shutil.rmtree(self.dataPath, ignore_errors=True)

            os.makedirs(self.dataPath, exist_ok=True)

        PivExecuteCompose.pivFilePath = dataPathRoot + 'default/'


        self.makeNewDataFolder()

        self.runstate.get_configuration()['name'] = self.runstate.get_configurationName()
        config = json.dumps(self.runstate.get_configuration(), indent=4)

        with open(PivExecuteCompose.pivFilePath + "configuration.json", "w") as outfile:
            outfile.write(config)

        with open(PivExecuteCompose.pivFilePath + "RunIndex.csv", "w") as outfile:
            outfile.write("Time Stamp,Type,File\n")

    def stop_deployment(self):
        PivExecuteCompose.diagnostic.emit_status("Stopping deployment", logToProgress=True)
        requests.put(PivExecuteCompose.baseBackendUrl + '/piv/stop')
        if not self.runstate.is_test():
            self.runstate.running = False


    def makeNewDataFolder(self):
        data_folder = 'default'
        if self.runstate.is_test():
            data_folder = self.runstate.get_configurationName()
        else:
            utcDateTime = time.gmtime()
            data_folder = "{year:04d}-{month:02d}-{day:02d}_{hour:02d}.{minute:02d}.{second:02d}".format(year=utcDateTime.tm_year, month=utcDateTime.tm_mon, day=utcDateTime.tm_mday, hour=utcDateTime.tm_hour, minute=utcDateTime.tm_min, second=utcDateTime.tm_sec)

        PivExecuteCompose.pivFilePath = self.dataPath + data_folder + '/'

        if not os.path.exists(PivExecuteCompose.pivFilePath):
            os.makedirs(PivExecuteCompose.pivFilePath)

        PivExecuteCompose.diagnostic.start_new_run(self.runstate, self.dataPath if self.runstate.is_test() else self.pivFilePath)

