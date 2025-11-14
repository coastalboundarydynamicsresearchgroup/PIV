const fs = require('fs');


var singleton = require('./inprogress');
const inprogress = singleton.getInstance();
const commonKey = singleton.getCommonKey();


const configurationPath = '/piv/configuration/';


var putPivDeploy = async function(req, res) {
  const { configurationName } = req.params;
  console.log(`PUT deploy ${configurationName}`);

  let configuration = {};
  const configurationFile = configurationPath + configurationName + '.json';
  console.log(`Loading configuration ${configurationFile}`);
  if (fs.existsSync(configurationFile)) {
    const runfile = { "configurationName": configurationName };
    const runFilePath = configurationPath + '__runfile__.deploy';
    fs.writeFileSync(runFilePath, JSON.stringify(runfile));
    console.log(`Deploying configuration: ${configurationName}`);
    inprogress[commonKey].status = `Deploying configuration ${configurationName}`;
    inprogress[commonKey].deploying = true;
  }
  else {
    console.log(`Not deploying, configuration ${configurationName} does not exist`);
    inprogress[commonKey].status = `Not deploying configuration ${configurationName}, file does not exist`;
    inprogress[commonKey].deploying = false;
  }

  var response = {
    progress: inprogress[commonKey],
    response: `Started piv deploy with configuration ${configurationName}`,
    status: 201
  };
  res.json(response);
}

var putPivUndeploy = async function(req, res) {
  console.log(`PUT undeploy`);

  const runFilePath = configurationPath + '__runfile__.deploy';
  if (fs.existsSync(runFilePath)) {
    fs.unlinkSync(runFilePath);
    console.log(`Undeployed all configurations`);
  }

  inprogress[commonKey].status = `Undeploying all configurations`;
  inprogress[commonKey].deploying = false;
  
  var response = {
    progress: inprogress[commonKey],
    response: `Stopped all piv deploy configurations`,
    status: 201
  };
  res.json(response);
}

module.exports = {putPivDeploy, putPivUndeploy};

