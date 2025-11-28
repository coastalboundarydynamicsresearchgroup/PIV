const fs = require('fs');


var singleton = require('./inprogress');
const inprogress = singleton.getInstance();
const commonKey = singleton.getCommonKey();


const configurationPath = '/piv/configuration/';

// TODO : Load this from some file
var testSteppings = {
  "CameraGain": {
    "start": 0,
    "end": 47,
    "step": 5,
  }
}

var putPivTest = async function(req, res) {
  const { configurationName } = req.params;
  console.log(`PUT test ${configurationName}`);

  let configuration = {};

  const configurationFile = configurationPath + configurationName + '.json';
  console.log(`Loading configuration ${configurationFile}`);

  if (fs.existsSync(configurationFile)) {
    configuration = JSON.parse(fs.readFileSync(configurationFile, 'utf8'));
    const runFileSet = GenerateTestConfigurations(configuration, testSteppings);
    const runfile = { "configurationName": runFileSet };
    const runFilePath = configurationPath + '__runfile__.deploy';
    fs.writeFileSync(runFilePath, JSON.stringify(runfile));
    console.log(`Testing configuration: ${configurationName}`);
    inprogress[commonKey].status = `Testing configuration ${configurationName}`;
    inprogress[commonKey].deploying = true;
  }
  else {
    console.log(`Not testing, configuration ${configurationName} does not exist`);
    inprogress[commonKey].status = `Not testing configuration ${configurationName}, file does not exist`;
    inprogress[commonKey].deploying = false;
  }

  var response = {
    progress: inprogress[commonKey],
    response: `Started piv test with configuration ${configurationName}`,
    status: 201
  };
  res.json(response);
}

var putPivStopTest = async function(req, res) {
  console.log(`PUT stop all tests`);

  const runFilePath = configurationPath + '__runfile__.deploy';
  if (fs.existsSync(runFilePath)) {
    fs.unlinkSync(runFilePath);
    console.log(`Stopping test of all configurations`);
  }
  CleanOldTestConfigurations();

  inprogress[commonKey].status = `Stopping test of all configurations`;
  inprogress[commonKey].deploying = false;
  
  var response = {
    progress: inprogress[commonKey],
    response: `Stopped all piv test configurations`,
    status: 201
  };
  res.json(response);
}

var GenerateTestConfigurations = function(configuration, steppings) {
  CleanOldTestConfigurations();

  var configurationNames = [];

  for (const [key, value] of Object.entries(steppings)) {
    if (configuration.hasOwnProperty(key)) {
      const start = value["start"];
      const end = value["end"];
      const step = value["step"];

      const savedValue = configuration[key];

      for (let currentValue = start; currentValue < end; currentValue += step) {
        configuration[key] = currentValue;
        const configName = `__test_${key}_${currentValue}__`;
        const configurationFile = configurationPath + configName + '.json';
        fs.writeFileSync(configurationFile, JSON.stringify(configuration));
        configurationNames.push(configName);
      }

      configuration[key] = savedValue;
    }
  }

  return configurationNames;
}

var CleanOldTestConfigurations = function() {
  const files = fs.readdirSync(configurationPath);
  for (const file of files) {
    if (file.startsWith('__test') && file.endsWith('.json')) {
      fs.unlinkSync(configurationPath + file);
    }
  }
}



// This actually goes in serialization helper?
var CreateCleanTestFolder = function(folderPath) {
  if (fs.existsSync(folderPath)) {
    fs.rmdirSync(folderPath, { recursive: true });
  }
  fs.mkdirSync(folderPath);
}

module.exports = {putPivTest, putPivStopTest};

