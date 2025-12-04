import os
import glob
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


configurationpath = '/pivdata/configuration'


class RunState:
    def __init__(self):
        self.Reset()

    def Reset(self):
        self.configurationName = ''
        self.configuration = {}
        self.running = False
        self.runChange = False
        self.test = False

    def is_running(self):
        return self.running
    
    def is_runchange(self):
        return self.runChange

    def is_test(self):
        return self.test

    def get_configurationName(self):
        if isinstance(self.configurationName, list):
            return ', '.join(self.configurationName)
        return self.configurationName
    
    def get_configuration(self):
        return self.configuration


class DeployHandler(FileSystemEventHandler):
    def __init__(self):
        self.runstate = RunState()

    def on_created(self, event):
        print('File created event: ' + event.src_path)
        self.handleNewOrModified(event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            return
        
        print('File modified event: ' + event.src_path)
        self.handleNewOrModified(event.src_path)

    def on_deleted(self, event):
        self.handleDeleted(event.src_path)

    def handleNewOrModified(self, path):
        if path[-18:] == "__runfile__.deploy":
            print('Handling new runfile, reevaluating')
            self.reevaluate(path)
        elif path[-21:] == "__immediate__.execute":
            self.executeImmediate(path)

    def handleDeleted(self, path):
        if path[-18:] == "__runfile__.deploy":
            self.runstate.running = False

    def reevaluate(self, runFilePath):
        configurationName = None
        running = False

        try:
            with open(runFilePath, 'r') as runfile:
                runData = json.load(runfile)
                if 'configurationName' in runData:
                    configurationName = runData['configurationName']
                    running = True
        except Exception:
            pass

        runChange = False
        if self.runstate.running != running:
            runChange = True

        self.runstate.configurationName = configurationName
        self.runstate.running = running
        self.runstate.runChange = runChange
        print('Run state: ' + self.runstate.get_configurationName() + ' Running' if self.runstate.running else ' NOT Running' + ' runchange ' if self.runstate.runChange else ' NOT runchange ' + str(self.runstate.configuration))

    def executeImmediate(self, executeFilePath):
        # TODO - Execute the immediate command
        os.remove(executeFilePath)


class Watcher:

    def __init__(self, runHandler, debug):
        self.runHandler = runHandler
        self.debug = debug
        self.observer = Observer()
        self.handler = DeployHandler()
        self.directory = configurationpath

    def run(self):
        self.observer.schedule(self.handler, self.directory, recursive=True)
        self.observer.start()
        print("\nWatcher Running in {}/\n".format(self.directory))
        #try:
        while True:
            time.sleep(0.1)
            if self.handler.runstate.is_running():
                self.execute_configurations()
        #except:
        #    self.observer.stop()

        self.observer.join()
        print("\nWatcher Terminated\n")

    def execute_configurations(self):
        if isinstance(self.handler.runstate.configurationName, list):
            self.handler.runstate.test = True
            doDelay = True
            for configName in self.handler.runstate.configurationName:
                # Every time self.runHandler (below) completes, the running flag will be false.
                if self.handler.runstate.is_test():
                    self.handler.runstate.running = True

                self.load_configuration(configName)
                if self.handler.runstate.is_running():
                    print(f'Runstate is running for test, calling run handler for {configName}')
                    self.runHandler(self.handler.runstate, doDelay)

                # Only delay for the first test in the run.
                doDelay = False
            self.clean_old_test_configurations()

        elif isinstance(self.handler.runstate.configurationName, str):
            self.load_configuration(self.handler.runstate.configurationName)
            if self.handler.runstate.is_running():
                print('Runstate is running, calling run handler')
                self.runHandler(self.handler.runstate, doDelay=True)

        print('Run is complete, resetting runstate')

        self.handler.runstate.Reset()


    def load_configuration(self, configurationName):
        fullpathname = configurationpath + '/' + configurationName + ".json"
        if os.path.isfile(fullpathname):
            print(f'Loading configuration {fullpathname}')
            with open(fullpathname, 'r') as configfile:
                self.handler.runstate.configuration = json.load(configfile)
        else:
            self.handler.runstate.running = False
            self.handler.runstate.runChange = False

    def clean_old_test_configurations(self):
        full_pattern = os.path.join(configurationpath, "__test*.json")

        # List files matching the pattern
        test_files = glob.glob(full_pattern)        
        for test_file in test_files:
            if os.path.isfile(test_file):  # Ensure it's a file, not a subdirectory
                try:
                    os.remove(test_file)
                    print(f"Deleted: {test_file}")
                except OSError as e:
                    print(f"Error deleting {test_file}: {e}")
