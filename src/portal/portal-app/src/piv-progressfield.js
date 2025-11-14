import { useState, useEffect } from 'react';
import './App.css';
import configuration from './configuration/configuration.json';
const baseBackendUrl = 'http://' + configuration.services.backend.host + ':' + configuration.services.backend.port;


const PivProgressField = ({fieldname, fieldTitle, initialValue}) => {

    return (
      <div className="progressfield">
        {fieldTitle}
        <input id={fieldname} type="text" defaultValue={initialValue} disabled={false}></input>
      </div>
    )
}

export default PivProgressField;
