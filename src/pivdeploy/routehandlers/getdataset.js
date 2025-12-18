/*
const { exec } = require("child_process");
const JSZip = require("jszip");
const fs = require("fs");
const path = require("path");
var singleton = require('./inprogress');
const { error } = require("console");
const { response } = require("express");
const inprogress = singleton.getInstance();
const commonKey = singleton.getCommonKey();
*/

const { exec } = require("child_process");
const fs = require("fs");
var singleton = require('./inprogress');
const inprogress = singleton.getInstance();
const commonKey = singleton.getCommonKey();

//
// Handle the web API route used to request all sonar881 configurations.
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


/*
const zipFolder = (folderPath, zipFilePath) => {
  const zip = new JSZip();

  const addFilesToZip = (zipFile, folderPath, currentPath = "") => {
    const files = fs.readdirSync(path.join(folderPath, currentPath));

    for (const file of files) {
      const filePath = path.join(currentPath, file);
      const fullFilePath = path.join(folderPath, filePath);
      const stats = fs.statSync(fullFilePath);

      if (stats.isDirectory()) {
        addFilesToZip(zipFile, folderPath, filePath);
      } else {
        fileContent = fs.readFileSync(fullFilePath);
        zipFile.file(filePath, fileContent);
      }
    }
  };

  result = {response: "", error: ""};
  addFilesToZip(zip, folderPath);
  zip
    .generateAsync({ type: "nodebuffer" })
    .then((content) => {
      fs.writeFileSync(zipFilePath, content);
      if (result.error === "") {
        result.response = `Zip file created at: ${zipFilePath}`;
        result.filename = path.basename(zipFilePath);
      }
      return result;
    })
    .catch((error) => result.error = error);;
};



//
// Handle the web API route used to request all acquired PIV data
// from the backend. This is used to create a zip file of all
// acquired data from the PIV system. The zip file is created
// and its file name returned to the client.
//
var getDataset = function(req, res) {
  console.log(`GET zipped dataset`);

  inprogress[commonKey].status = `Archiving PIV data in zip file . . .`;
  now = new Date(Date.now());
  utcMonth = `${now.getUTCMonth()+1}`.padStart(2, '0');
  utcDate = `${now.getUTCDate()}`.padStart(2, '0');
  utcHour = `${now.getUTCHours()}`.padStart(2, '0');
  utcMinute = `${now.getUTCMinutes()}`.padStart(2, '0');
  utcSecond = `${now.getUTCSeconds()}`.padStart(2, '0');
  const zipFileName = `pivArchive_${now.getUTCFullYear()}-${utcMonth}-${utcDate}_${utcHour}.${utcMinute}.${utcSecond}.zip`;
  const zipFilePath = path.join(`/piv/archive/${zipFileName}`);
  result = zipFolder('/piv/data/test/', zipFilePath)
  
  
  if (result.error !== "") {
    inprogress[commonKey].status = `Error archiving PIV data: ${result.error}`;
    console.log(`error: ${result.error}`);
    if (stderr) {
      console.log(`stderr: ${stderr}`);
    }
    res.status(500).send(result.error);
  } else {
    inprogress[commonKey].status = `PIV data in zipped in file ${zipFilePath}`;
    console.log(`Dataset zipped: ${zipFilePath}`);
    res.set('Access-Control-Allow-Origin', '*');
    //res.json(zipFilePath);
    res.json(result);
  }
}

module.exports = getDataset;
*/
