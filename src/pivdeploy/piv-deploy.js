const express = require('express');
const http = require('http');
const bodyParser = require('body-parser');
const cors = require("cors"); // enforce CORS, will be set to frontend URL when deployed

const fs = require('fs');

const getConfigurations = require('./routehandlers/getconfigurations');
const putconfiguration = require('./routehandlers/putconfiguration');
const getconfiguration = require('./routehandlers/getconfiguration');
const deleteconfiguration = require('./routehandlers/deleteconfiguration');
const getDataset = require('./routehandlers/getdataset');
const {putPivDeploy, putPivUndeploy} = require('./routehandlers/putpivdeploy');
const getDeployProgress = require('./routehandlers/getdeployprogress');
const putPivProgress = require('./routehandlers/putpivprogress');


let rawdata = fs.readFileSync('/configuration/configuration.json');
configuration = JSON.parse(rawdata);
console.log(configuration);

const app = express();
app.use(cors());

const router = express.Router();

// Get the list of configurations that currently exist.
router.get('/configurations', [getConfigurations]);

// Put the content of the specified configuration under the specified name.
router.put('/configuration/:configurationName', [putconfiguration]);

// Get the content of the specified configuration under the specified name.
router.get('/configuration/:configurationName', [getconfiguration]);

// Delete the content of the specified configuration under the specified name.
router.delete('/configuration/:configurationName', [deleteconfiguration]);

// Get the zipped data results from any and all previous deployments.
router.get('/dataset', [getDataset]);

// Put the command to execute with the specified configuration.
router.put('/piv/execute/:configurationName', [putPivDeploy]);

// Put the command to stop any previously executed configuration.
router.put('/piv/stop', [putPivUndeploy]);

// Get the deploy progress.
router.get('/piv/execute/progress', [getDeployProgress]);

// Put progress from the execute or other backend process.
router.put('/piv/progress/:id', [putPivProgress]);


var server = http.createServer(app);
const PORT = 5000;
app.use(bodyParser.json());
app.use('/', router);
app.use(express.static('public'));

server.listen(PORT, () => console.log(`Server running on port http://model-packager:${PORT}`));
