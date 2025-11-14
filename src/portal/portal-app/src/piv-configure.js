import { useState, useEffect } from 'react';
import './App.css';
import { DistributeConfiguration, WriteConfiguration, DeleteConfiguration } from './piv-configpersist';
import PivProgressPollerSingleton from './piv-progresspoller';
import configuration from './configuration/configuration.json';
import PivConfigButtons from './piv-configbuttons'
const baseBackendUrl = 'http://' + configuration.services.backend.host + ':' + configuration.services.backend.port;


const PivConfigure = ({getState, setState, deploying, deployrunning, onTestClicked, onPingData, test, connectionstyle, setconnectionstyle}) => {
  const [configurations, setConfigurations] = useState([]);
  const [configurationChanged, setConfigurationChanged] = useState(0);
  const [selectedConfiguration, setSelectedConfiguration] = useState(0);

  useEffect(() => {
    const messages = document.getElementById('messages');
    fetch(baseBackendUrl + '/configurations', { method: 'GET', mode: 'cors' })
    .then(data => data.json())
    .then(response => {
      setConfigurations([...response]);
      if (messages) {
        messages.value += 'Retrieved configurations ' + response + '\n'
      }
      document.getElementById("configurationsselectlist").selectedIndex = selectedConfiguration;
      const configName = document.getElementById("configurationsselectlist").value;
      document.getElementById("newconfiguration").value = configName;
      if (configName) {
        fetch(baseBackendUrl + '/configuration/' + configName, { method: 'GET', mode: 'cors' })
        .then(data => data.json())
        .then(response => {
          DistributeConfiguration(setconnectionstyle, response);
          setState('nametouched', false);
          setState('valuetouched', false);
          if (messages) {
            messages.value += `Retrieved configuration ${configName}\n`;
          }
        });
      }
    });
  }, [configurationChanged, selectedConfiguration]);
  
  const onCreate = () => {
    WriteConfiguration(connectionstyle, () => {
      setConfigurationChanged(configurationChanged + 1);
    });
  }

  const onSave = () => {
    WriteConfiguration(connectionstyle, () => {
      setConfigurationChanged(configurationChanged + 1);
    });
  }
  
  const onDelete = () => {
    DeleteConfiguration(() => {
      setSelectedConfiguration(0);
      setConfigurationChanged(configurationChanged + 1);
    });
  }

  const onDeploy = () => {
    console.log(`Deploying configuration`);
    GetDeployResponse();
  }

  const onDownload = () => {
    var init = {
      method: 'GET',
      mode: 'cors',
      headers: {
        'Content-type': 'application/json'
      }
    };
    
    fetch(baseBackendUrl + '/dataset', init)
    .then(data => data.json())
    .then(response => {
      console.log(response)
      const fileName = response.filename + '.zip';
      const aTag = document.createElement("a");
      aTag.href = "/piv/archive/" + fileName;         // Root '/' is the nodejs /public folder
      aTag.setAttribute("download", "/piv/archive/" + fileName);
      document.body.appendChild(aTag);
      aTag.click();
      aTag.remove();
    });
  }

  const GetDeployResponse = () => {
    const messages = document.getElementById('messages');

    var init = {
      method: 'PUT',
      mode: 'cors',
      headers: {
        'Content-type': 'application/json'
      }
    };
    
    var deployFlag = true;
    var progressSingleton = PivProgressPollerSingleton.getInstance();
    if (progressSingleton.progress) {
      deployFlag = !progressSingleton.progress.deploying && !progressSingleton.progress.deployrunning;
    }
  
    const configurationName = document.getElementById("newconfiguration").value;
    const commandUrl = deployFlag ? '/piv/execute/' + configurationName : '/piv/stop'
    fetch(baseBackendUrl + commandUrl, init)
    .then(data => data.json())
    .then(response => {
      if (response.status === 201) {
        messages.value += 'Sent execute/stop command with status ' + response.status + '\n';
        messages.value += response.response + '\n';
        if (response.progress) {
          console.log(`Got execute/stop response ${response.progress.deploying} and running ${response.progress.deployrunning}`);
          deployFlag = !response.progress.deploying /*&& !response.progress.deployrunning*/;
        }
      }
      else {
        messages.value += 'Error sending execute/stop command with status ' + response.status + '\n';
      }
    });
  }

  const handleConfigurationSelectionClick = (selectedConfiguration) => {
    const messages = document.getElementById('messages');

    const clickedConfiguration = document.getElementById("configurationsselectlist").value;
    setSelectedConfiguration(document.getElementById("configurationsselectlist").selectedIndex);

    document.getElementById("newconfiguration").value = clickedConfiguration;
    setState('nametouched', false);

    messages.value += `Selected configuration ${clickedConfiguration}\n`;
  }

    
  return (
    <div className="configuration-management">
      <div className="configuration-controls">
        <input id="newconfiguration" type="text" onChange={() => setState('nametouched', true)}></input>
        Configurations
        <select name="configurationsselectlist" id="configurationsselectlist" onChange={handleConfigurationSelectionClick} size="13">
          {configurations.map(configuration => (
            <option key={configuration} value={configuration}>{configuration}</option>
          ))}
        </select>
      </div>
      <PivConfigButtons deploying={deploying} deployrunning={deployrunning} getStateFunc={getState} onCreateFunc={onCreate} onSaveFunc={onSave} onDeleteFunc={onDelete} onDeployFunc={onDeploy} onDownloadFunc={onDownload} onTestClicked={onTestClicked} test={test} />
    </div>
  )
}



export default PivConfigure;
