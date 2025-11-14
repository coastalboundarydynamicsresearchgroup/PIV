import { useState, useEffect } from 'react';
import './App.css';

import configuration from './configuration/configuration.json';
const baseBackendUrl = 'http://' + configuration.services.backend.host + ':' + configuration.services.backend.port;


const PollProgress = () => {
    const messages = document.getElementById('messages');
    fetch(baseBackendUrl + '/piv/execute/progress', { method: 'GET', mode: 'cors' })
    .then(data => data.json())
    .then(response => {
      if (messages) {
        // TODO
      }
      /*
      const progressfield = document.getElementById('progress');
      if (progressfield && response.status) {
        progressfield.value = response.status;
      }
      */
      PivProgressPollerSingleton.instance.progress = response;
      if (PivProgressPollerSingleton.progressFunc) {
        PivProgressPollerSingleton.progressFunc(response);
      }
    });

    setTimeout(PollProgress, 1000);
}


class progressPoller {
  constructor() {
    console.log(`progressPoller launching poll`);
    PollProgress();
  }
}

class PivProgressPollerSingleton {
  constructor() {
    throw new Error('Use PivProgressPollerSingleton.getInstance()');
  }
  
  static getInstance(updateProgressFunc=null) {
    if (updateProgressFunc) {
      PivProgressPollerSingleton.progressFunc = updateProgressFunc;
    }

    if (!PivProgressPollerSingleton.instance) {
      PivProgressPollerSingleton.instance = new progressPoller();
    }
    return PivProgressPollerSingleton.instance;
  }
}

export default PivProgressPollerSingleton;
