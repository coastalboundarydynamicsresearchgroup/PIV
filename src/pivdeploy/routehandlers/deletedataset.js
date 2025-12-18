const fs = require("fs");

const datasetdirectory = '/piv/data/';

//
// Handle the web API route used to delete the specified PIV configurations.
//
var deleteDataset = function(req, res) {
  const { datasetName } = req.params;
  console.log(`DELETE dataset ${datasetName}`);

  fs.rm(datasetdirectory + datasetName, { recursive: true, force: true }, (err) => {
    if (err) {
      console.error('Error deleting dataset directory:', err);
      res.status(500).send('Error deleting dataset directory');
      return;
    }
    console.log(`Deleted dataset: ${datasetdirectory}${datasetName}`);
    res.set('Access-Control-Allow-Origin', '*');
    var response = {
      response: `Dataset ${datasetName} deleted`,
      status: 201
    };
    res.json(response);
  }
  );
}

module.exports = deleteDataset;
