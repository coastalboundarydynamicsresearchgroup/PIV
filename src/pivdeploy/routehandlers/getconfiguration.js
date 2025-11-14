const fs = require('fs');

const configurationdirectory = '/piv/configuration/';

//
// Handle the web API route used to request a PIV configurations.
//
var getConfiguration = function(req, res) {
  fs.readFile(configurationdirectory + req.params.configurationName + '.json', 'utf8', (err, data) => {
    if (err) {
      console.error('Error reading file:', err);
      res.status(500).send('Error reading file');
      return;
    }
    console.log(`Found configuration: ${data}`);
    res.set('Access-Control-Allow-Origin', '*');
    res.json(JSON.parse(data));
  }
  );
}

module.exports = getConfiguration;
