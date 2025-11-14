const fs = require("fs");

const configurationdirectory = '/piv/configuration/';

//
// Handle the web API route used to delete the specified PIV configurations.
//
var deleteConfigurations = function(req, res) {
  const { configurationName } = req.params;
  console.log(`DELETE configuration ${configurationName}`);

  fs.unlink(configurationdirectory + configurationName + '.json', (err) => {
    if (err) {
      console.error('Error deleting file:', err);
      res.status(500).send('Error deleting file');
      return;
    }
    console.log(`Deleted configuration: ${configurationdirectory}${configurationName}.json`);
    res.set('Access-Control-Allow-Origin', '*');
    var response = {
      response: `Configuration ${configurationName} deleted`,
      status: 201
    };
    res.json(response);
  }
  );
}

module.exports = deleteConfigurations;
