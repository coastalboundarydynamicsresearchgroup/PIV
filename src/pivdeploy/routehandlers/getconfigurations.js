const fs = require('fs');
const path = require('path');

const configurationdirectory = '/piv/configuration/';

//
// Handle the web API route used to request the names of all PIV configurations.
//
var getConfigurations = function(req, res) {
  console.log(`GET configuration names`);

  fs.readdir(configurationdirectory, (err, files) => {
    if (err) {
      console.error('Error reading directory:', err);
      res.status(500).send('Error reading directory');
      return;
    }

    const configurationFiles = files.filter(file => path.extname(file) === '.json');
    const configurationNames = configurationFiles.map(file => path.basename(file, '.json'));

    console.log(`Found configuration names: ${configurationNames}`);
    res.set('Access-Control-Allow-Origin', '*');
    res.json(configurationNames);
  });
}

module.exports = getConfigurations;
