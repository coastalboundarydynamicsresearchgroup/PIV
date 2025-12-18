const { exec } = require("child_process");
const JSZip = require("jszip");
const fs = require("fs");
const path = require("path");
var singleton = require('./inprogress');
const { error } = require("console");
const { response } = require("express");
const archiver = require('archiver');
const inprogress = singleton.getInstance();
const commonKey = singleton.getCommonKey();


//
// Handle the web API route used to request all acquired PIV data
// from the backend. This is used to create a zip file of all
// acquired data from the PIV system. The zip file is created
// and its file name returned to the client.
//
/*
var getPivArchiveFile = function(req, res) {
  archiveFilename = req.params.filename

  console.log(`GET archived dataset file: ${archiveFilename}`);

  inprogress[commonKey].status = `Archiving PIV data in zip file . . .`;
  const zipFilePath = path.join('/', 'piv', 'archive', archiveFilename);
  console.log(`Zip file path: ${zipFilePath}`);
  
  // Ensure the file exists
  if (!fs.existsSync(zipFilePath)) {
    return res.status(404).send('File not found');
  }

  // Set headers for the response
  res.writeHead(200, {
    'Content-Type': 'application/zip',
    'Content-Disposition': `attachment; filename=${archiveFilename + ".zip"}`, // Suggests a filename for download
    'Content-Length': fs.statSync(zipFilePath).size // Optional, but good practice
  });

  // Create a readable stream and pipe it to the response
  const readStream = fs.createReadStream(zipFilePath);
  readStream.pipe(res);

  // Optional: clean up the file after the stream closes if it was temporary
  readStream.on('close', () => {
    // fs.unlinkSync(filePath); // Uncomment to delete the file after sending
  });

}
*/

const addFilesToZip = (archive, folderPath, currentPath = "") => {
  console.log(`Adding files from folder: ${path.join(folderPath, currentPath)}`);
  const files = fs.readdirSync(path.join(folderPath, currentPath));

  for (const file of files) {
    const filePath = path.join(currentPath, file);
    const fullFilePath = path.join(folderPath, filePath);
    const stats = fs.statSync(fullFilePath);

    if (stats.isDirectory()) {
      addFilesToZip(archive, folderPath, filePath);
    } else {
      console.log(`Adding file to archive: ${fullFilePath}`);
      archive.file(fullFilePath, { name: file }); // Add a file from disk
    }
  }
};


var getPivArchiveFile_dynamic = function(req, res) {
  // Set response headers
  now = new Date(Date.now());
  utcMonth = `${now.getUTCMonth()+1}`.padStart(2, '0');
  utcDate = `${now.getUTCDate()}`.padStart(2, '0');
  utcHour = `${now.getUTCHours()}`.padStart(2, '0');
  utcMinute = `${now.getUTCMinutes()}`.padStart(2, '0');
  utcSecond = `${now.getUTCSeconds()}`.padStart(2, '0');
  const zipFileName = `pivTest_${now.getUTCFullYear()}-${utcMonth}-${utcDate}_${utcHour}.${utcMinute}.${utcSecond}.zip`;
  res.set({
    'Content-Type': 'application/zip',
    'Content-Disposition': 'attachment; filename=' + zipFileName
  });

  const archive = archiver('zip', {
    zlib: { level: 9 } // Sets the compression level
  });

  // Pipe the archive data to the response
  archive.pipe(res);
  const folderPath = path.join('/', 'piv', 'data', 'test');

  // Add files/data to the archive
  addFilesToZip(archive, folderPath);

  // Finalize the archive (sets the end of the stream)
  archive.finalize();

  // Handle errors during zipping/streaming
  archive.on('error', (err) => {
    res.status(500).send({ error: err.message });
  });

}

module.exports = getPivArchiveFile_dynamic;
