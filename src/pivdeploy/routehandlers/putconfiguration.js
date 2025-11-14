const fs = require("fs");

const configurationdirectory = '/piv/configuration/';

//
// Handle the web API route used to put the content of a PIV configuration
// to backing store.
//
var putConfiguration = function(req, res) {
  const { configurationName } = req.params;
  req.body["Name"] = configurationName;
  var configuration_raw = JSON.stringify(req.body);
  if (!configuration_raw) {
    configuration_raw = '{"Name": ${configurationname},"CycleCount": 1,"ShutterOpenTime": 100,"DwellTime": 25,"CyclePauseTime": 50,"DebugMultiplier": 1}'
  }


  try {
    fs.writeFileSync(configurationdirectory + configurationName + '.json', configuration_raw, 'utf8');
    console.log(`Wrote configuration: ${configurationdirectory}${configurationName}.json`);
    res.set('Access-Control-Allow-Origin', '*');
    var response = {
      response: `Configuration ${configurationName} saved`,
      status: 201
    };
    res.json(response);
  } catch (err) {
    console.error('Error writing file:', err);
    res.status(500).send('Error writing file');
    return;
  }
}

module.exports = putConfiguration;

