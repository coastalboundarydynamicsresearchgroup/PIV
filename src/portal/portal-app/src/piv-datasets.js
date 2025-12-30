import './App.css';
import { useState, useEffect } from 'react';

import configuration from './configuration/configuration.json';
const baseBackendUrl = 'http://' + configuration.services.backend.host + ':' + configuration.services.backend.port;


const PivDatasets = () => {
  const [datasets, setDatasets] = useState([]);
  const [datasetsChanged, setdatasetsChanged] = useState(0);
  const [selectedDataset, setSelectedDataset] = useState(0);

  useEffect(() => {
    const messages = document.getElementById('messages');
    fetch(baseBackendUrl + '/datasets', { method: 'GET', mode: 'cors' })
    .then(data => data.json())
    .then(response => {
      setDatasets([...response]);
      if (messages) {
        messages.value += 'Retrieved datasets ' + response + '\n'
      }
      document.getElementById("datasetselectlist").selectedIndex = selectedDataset;
      const datasetName = document.getElementById("datasetselectlist").value;
    });
  }, [datasetsChanged, selectedDataset]);


  const onDelete = () => {
    DeleteDataset(() => {
      setSelectedDataset(0);
      setdatasetsChanged(datasetsChanged + 1);
    });
  }

  const DeleteDataset = (onDoneHandler) => {
    const messages = document.getElementById('messages');
  
    var init = {
      method: 'DELETE',
      mode: 'cors',
      headers: {
        'Content-type': 'application/json'
      }
    };
    
    const datasetName = document.getElementById("datasetselectlist").value;
    fetch(baseBackendUrl + '/dataset/' + datasetName, init)
    .then(data => data.json())
    .then(response => {
      if (response.status === 201) {
        messages.value += 'Deleted dataset with status ' + response.status + '\n';
      }
      else {
        messages.value += 'Error deleting dataset with status ' + response.status + '\n';
      }
      onDoneHandler();
    });
  }
  

  const OnDownload = () => {
    DownloadDataset(() => {
    });
  }

  const DownloadDataset = (onDoneHandler) => {
    const messages = document.getElementById('messages');
  
    var init = {
      method: 'GET',
      mode: 'cors',
      headers: {
        'Content-type': 'application/json'
      }
    };
    
    const datasetName = document.getElementById("datasetselectlist").value;
    fetch(baseBackendUrl + '/dataset/' + datasetName, init)
    .then(data => data.json())
    .then(response => {
      if (response.status === 201) {
        messages.value += 'Started dataset download with status ' + response.status + '\n';
        const zippedFilePath = `/piv/archive/${response.filename}.zip`;

        console.log(response)
        const fileName = response.filename + '.zip';
        const aTag = document.createElement("a");
        aTag.href = "/piv/archive/" + fileName;         // Root '/' is the nodejs /public folder
        aTag.setAttribute("download", fileName);
        document.body.appendChild(aTag);
        aTag.click();
        aTag.remove();
      }
      onDoneHandler();
    });
  }
  


  return (
    <div className="configuration-buttons">
      Datasets
      <select name="datasetselectlist" id="datasetselectlist" size="13">
        {datasets.map(dataset => (
        <option key={dataset} value={dataset}>{dataset}</option>
        ))}
      </select>
      <div className="configuration-buttonrow">
        <button type="button" id="download-button"  onClick={OnDownload}>
          Download Data
        </button>
        <button type="button" id="remove-button" onClick={onDelete}>
          Delete Data
        </button>
      </div>
    </div>
  );
}

export default PivDatasets;

