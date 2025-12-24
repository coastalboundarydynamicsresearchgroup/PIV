import os
import time
import json
import glob
from shutil import make_archive

from diagnostics import DiagnosticSingleton
from picoexecutecompose import PicoExecuteCompose

configurationpath = '/pivdata/configuration'
testdatapath = '/pivdata/data/test'
archivepath = '/pivdata/archive'


class DeployRunner:
    diagnostic = DiagnosticSingleton.get_instance()

    def __init__(self, runstate):
        self.runstate = runstate

    def execute_configurations(self):
        if isinstance(self.runstate.configurationName, list):
            self.runstate.test = True
            DeployRunner.diagnostic.emit_status(f'Starting test for configuration "{self.runstate.get_configurationName()}"', logToProgress=True, options={'count':0})
            for configName in self.runstate.configurationName:
                # Every time self.execute_deploy (below) completes, the running flag will be false.
                if self.runstate.is_test():
                    self.runstate.running = True

                self.load_configuration(configName)
                if self.runstate.is_running():
                    DeployRunner.diagnostic.emit_status(f'Testing using stepping configuration "{configName}"', logToProgress=True, options={'count':self.runstate.testScanNumber})
                    self.execute_deploy()
                    self.runstate.testScanNumber += 1

            self.clean_old_test_configurations()
            self.zip_test_results()

        elif isinstance(self.runstate.configurationName, str):
            self.load_configuration(self.runstate.configurationName)
            if self.runstate.is_running():
                DeployRunner.diagnostic.emit_status(f'Executing configuration "{self.runstate.get_configurationName()}"', logToProgress=True)
                self.execute_deploy()

        print('Run is complete, resetting runstate')

        DeployRunner.diagnostic.emit_status("Deployment for configuration '" + self.runstate.get_configurationName() + "' finished", logToProgress=True, options={'deploying':False,'deployrunning':False})
        self.runstate.Reset()

    def execute_deploy(self):
        deployer = PicoExecuteCompose(self.runstate)
        deployer.compose_and_execute()


    def load_configuration(self, configurationName):
        fullpathname = configurationpath + '/' + configurationName + ".json"
        if os.path.isfile(fullpathname):
            DeployRunner.diagnostic.emit_status(f'Loading configuration {fullpathname}')
            with open(fullpathname, 'r') as configfile:
                self.runstate.configuration = json.load(configfile)
            self.runstate.configurationName = configurationName
        else:
            self.runstate.running = False
            self.runstate.runChange = False

    def clean_old_test_configurations(self):
        full_pattern = os.path.join(configurationpath, "__test*.json")

        # List files matching the pattern
        test_files = glob.glob(full_pattern)        
        for test_file in test_files:
            if os.path.isfile(test_file):  # Ensure it's a file, not a subdirectory
                try:
                    os.remove(test_file)
                    DeployRunner.diagnostic.emit_status(f'Deleted test stepping configuration "{test_file}"')
                except OSError as e:
                    DeployRunner.diagnostic.emit_status(f'Error deleting test stepping configuraiton "{test_file}": {e}')

    def zip_test_results(self):
        global testdatapath
        global archivepath

        utcDateTime = time.gmtime()
        archiveFilename = "test_{year:04d}-{month:02d}-{day:02d}_{hour:02d}.{minute:02d}.{second:02d}".format(year=utcDateTime.tm_year, month=utcDateTime.tm_mon, day=utcDateTime.tm_mday, hour=utcDateTime.tm_hour, minute=utcDateTime.tm_min, second=utcDateTime.tm_sec)
        DeployRunner.diagnostic.emit_status("Test complete, archiving to '" + archiveFilename + "'", logToProgress=True)
        make_archive(archivepath + "/" + archiveFilename, "zip", testdatapath)

        return archiveFilename

