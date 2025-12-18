const { exec } = require("child_process");
const fs = require("fs");
var singleton = require('./inprogress');
const inprogress = singleton.getInstance();
const commonKey = singleton.getCommonKey();

//
// Handle the web API route used to zip a specified dataset.
// Pass the request to a python backend script, accepting the response
// through its stdout.
//
var getDataset = function(req, res) {
  const { datasetName } = req.params;
  console.log(`Get zipped dataset ${datasetName}`);

  inprogress[commonKey].status = `Archiving PIV dataset ${datasetName}. . .`;
  exec(`python zipdataset.py ${datasetName}`, (error, stdout, stderr) => {
    if (error) {
      inprogress[commonKey].status = `Error archiving PIV data: ${error.message}`;
      console.log(`error: ${error.message}`);
      if (stderr) {
        console.log(`stderr: ${stderr}`);
      }
      res.status(error.code).send(error.message)
    } else {
      const response = JSON.parse(stdout);
      inprogress[commonKey].status = `PIV data in zipped in file ${response.filename}`;
      res.set('Access-Control-Allow-Origin', '*');
      res.status(201);
      res.json(response);
    }
  });
}

module.exports = getDataset;
