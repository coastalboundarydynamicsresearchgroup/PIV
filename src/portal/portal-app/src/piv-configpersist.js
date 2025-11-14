import configuration from './configuration/configuration.json';
const baseBackendUrl = 'http://' + configuration.services.backend.host + ':' + configuration.services.backend.port;


const DistributeConfiguration = (setconnectionstyle, configuration) => {
  setconnectionstyle(configuration.ConnectionStyle);
  document.getElementById("minutes").value = configuration.Minutes;
  document.getElementById("debugbox").checked = configuration.Debug;
  document.getElementById("camerablacklevel").value = configuration.CameraBlacklevel;
  document.getElementById("cameragain").value = configuration.CameraGain;
  document.getElementById("cameragamma").value = configuration.CameraGamma;
  document.getElementById("shutteropentime").value = configuration.ShutterOpenTime;
  document.getElementById("laserontime").value = configuration.LaserOnTime;
  document.getElementById("imagecount").value = configuration.ImageCount;
  document.getElementById("imagerate").value = configuration.ImageRate;
  document.getElementById("framerate").value = configuration.FrameRate;
  document.getElementById("framecount").value = configuration.FrameCount;
}

var isValidInput = true;
const ValidateIntField = (fieldName, minValue, maxValue, increment=1) => {
  const messages = document.getElementById('messages');

  const fieldValue = document.getElementById(fieldName).value;
  if (isNaN(fieldValue)) {
    messages.value += `Invalid value ${fieldValue} in field ${fieldName}, not a number\n`;
    isValidInput = false;
    return minValue;
  }

  const parsedInt = parseInt(fieldValue);
  if (parsedInt < minValue) {
    messages.value += `Invalid value ${parsedInt} in field ${fieldName}, must be >= ${minValue}\n`;
    isValidInput = false;
    return minValue;
  }

  if (parsedInt > maxValue) {
    messages.value += `Invalid value ${parsedInt} in field ${fieldName}, must be <= ${maxValue}\n`;
    isValidInput = false;
    return maxValue;
  }

  if (parsedInt % increment !== 0) {
    messages.value += `Invalid value ${parsedInt} in field ${fieldName}, must be a multiple of ${increment}\n`;
    isValidInput = false;
    return minValue;
  }

  return parsedInt;
}

const ValidateFloatField = (fieldName, minValue, maxValue, increment) => {
  const messages = document.getElementById('messages');

  const fieldValue = document.getElementById(fieldName).value;
  if (isNaN(fieldValue)) {
    messages.value += `Invalid value ${fieldValue} in field ${fieldName}, not a number\n`;
    isValidInput = false;
    return minValue;
  }
  const parsedFloat = parseFloat(fieldValue);

  if (parsedFloat < minValue) {
    messages.value += `Invalid value ${parsedFloat} in field ${fieldName}, must be >= ${minValue}\n`;
    isValidInput = false;
    return minValue;
  }

  if (parsedFloat > maxValue) {
    messages.value += `Invalid value ${parsedFloat} in field ${fieldName}, must be <= ${maxValue}\n`;
    isValidInput = false;
    return maxValue;
  }

  const remainder = parsedFloat % increment;
  if (remainder > increment) {
    messages.value += `Invalid value ${parsedFloat} in field ${fieldName}, has remainder of ${remainder}, must be a multiple of ${increment}\n`;
    isValidInput = false;
    return minValue;
  }

  return parsedFloat;
}

const ValidateCheckField = (fieldName) => {
  const fieldValue = document.getElementById(fieldName).checked;
  return fieldValue;
}

const WriteConfiguration = (connectionstyle, onDoneHandler) => {
  isValidInput = true;

  const configuration = {};

  configuration.ConnectionStyle = connectionstyle;
  configuration.Minutes = ValidateFloatField("minutes", 0, 59, 0.1);
  configuration.Debug = ValidateCheckField("debugbox");
  configuration.CameraBlacklevel = ValidateIntField("camerablacklevel", 0, 100, 1);
  configuration.CameraGain = ValidateIntField("cameragain", 0, 47, 1);
  configuration.CameraGamma = ValidateFloatField("cameragamma", 0.5, 2.0, 0.1);
  configuration.ShutterOpenTime = ValidateIntField("shutteropentime", 2, 1000, 1);
  configuration.LaserOnTime = ValidateIntField("laserontime", 1, 1000, 1);
  configuration.ImageCount = ValidateIntField("imagecount", 2, 1000, 1);
  configuration.ImageRate = ValidateIntField("imagerate", 4, 1000, 1);
  configuration.FrameRate = ValidateIntField("framerate", 10, 1000, 1);
  configuration.FrameCount = ValidateIntField("framecount", 0, 1000000, 1);

  if (isValidInput) {
    PutConfiguration(configuration, onDoneHandler);
  }
}

const PutConfiguration = (configuration, onDoneHandler) => {
    const messages = document.getElementById('messages');

    var init = {
      method: 'PUT',
      mode: 'cors',
      headers: {
        'Content-type': 'application/json'
      },
      body: JSON.stringify(configuration)
    };
    
    const configName = document.getElementById("newconfiguration").value;
    fetch(baseBackendUrl + '/configuration/' + configName, init)
    .then(data => data.json())
    .then(response => {
      if (response.status === 201) {
        messages.value += 'Wrote configuration with status ' + response.status + '\n';
      }
      else {
        messages.value += 'Error writing configuration with status ' + response.status + '\n';
      }
      onDoneHandler();
    });
}

const DeleteConfiguration = (onDoneHandler) => {
  const messages = document.getElementById('messages');

  var init = {
    method: 'DELETE',
    mode: 'cors',
    headers: {
      'Content-type': 'application/json'
    }
  };
  
  const configName = document.getElementById("newconfiguration").value;
  fetch(baseBackendUrl + '/configuration/' + configName, init)
  .then(data => data.json())
  .then(response => {
    if (response.status === 201) {
      messages.value += 'Deleted configuration with status ' + response.status + '\n';
    }
    else {
      messages.value += 'Error deleting configuration with status ' + response.status + '\n';
    }
    onDoneHandler();
  });
}


export  { DistributeConfiguration, WriteConfiguration, DeleteConfiguration };
