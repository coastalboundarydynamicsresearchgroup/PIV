const fs = require('fs');
const path = require('path');

const datadirectory = '/piv/data/';

//
// Handle the web API route used to request the names of all PIV configurations.
//
var getDatasets = function(req, res) {
  console.log(`GET dataset names`);

  fs.readdir(datadirectory, (err, files) => {
    if (err) {
      console.error('Error reading directory:', err);
      res.status(500).send('Error reading directory');
      return;
    }

    const datasetDirectories = files.filter(file => (path.extname(file) !== '.json') && !file.startsWith('__'));

    console.log(`Found dataset names: ${datasetDirectories}`);
    res.set('Access-Control-Allow-Origin', '*');
    res.json(datasetDirectories);
  });
}

module.exports = getDatasets;
