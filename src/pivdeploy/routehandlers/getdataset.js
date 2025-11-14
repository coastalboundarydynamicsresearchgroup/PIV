const { exec } = require("child_process");
const JSZip = require("jszip");
const fs = require("fs");
const path = require("path");
var singleton = require('./inprogress');
const { error } = require("console");
const { response } = require("express");
const inprogress = singleton.getInstance();
const commonKey = singleton.getCommonKey();


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
    })
    .catch((error) => result.error = error);;

  if (result.error === "") {
    result.response = `Zip file created at: ${zipFilePath}`;
  }

  return result;
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
  result = zipFolder('/piv/data/', zipFilePath)
  
  
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
    res.json(zipFilePath);
  }
}

module.exports = getDataset;
