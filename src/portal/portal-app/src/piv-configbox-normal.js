import { useState, useEffect } from 'react';
import './App.css';
import PivConfigField from './piv-configfield';
import PivCheckBox from './piv-checkbox';
import PivRadioGroup from './piv-radiogroup';
import PivProgressField from './piv-progressfield';
import PivUpdateField from './piv-updatefield';
import PivStatusLed from './piv-statusled';

// If not used, delete this line
//const baseBackendUrl = 'http://' + configuration.services.backend.host + ':' + configuration.services.backend.port;


const PivConfigBoxNormal = ({deploying, deployrunning, connectionstyle, setconnectionstyle, onChangeFunc}) => {

  const radioOptions = [
    { label: 'Flir', value: 'flir' },
    { label: 'Pico', value: 'pico' },
  ];

  return (
        <div className="configurationbox">
          <div style={{fontSize: '18pt', padding: '18px'}} >Camera and Laser</div>

          <div className="configurationgroup">
            <div className="Connection Method">
              <PivRadioGroup name="connectionmethod" options={radioOptions} selectedValue={connectionstyle} setselectedValue={setconnectionstyle} onChange={onChangeFunc}/>
            </div>
            
            <fieldset style={{ border: '1px solid #ccc', padding: '1px', width: '99%', justifyContent: 'center' }}>
              <legend style={{ padding: '0 10px' }}>General</legend>
              <div className="configurationrow">
                <PivConfigField fieldname="minutes" fieldTitle="Delay to start (minutes)" initialValue="5" onChangeFunc={onChangeFunc}></PivConfigField>
                <PivCheckBox fieldname="debugbox" fieldTitle="Debug" initialValue="debug" onChangeFunc={onChangeFunc}></PivCheckBox>
              </div>
            </fieldset>
          </div>

          <div className="configurationgroup">
            <fieldset style={{ border: '1px solid #ccc', padding: '1px', width: '99%', justifyContent: 'center' }}>
              <legend style={{ padding: '0 10px' }}>Camera Settings</legend>
              <div className="configurationrow">
                <PivConfigField fieldname="camerablacklevel" fieldTitle="Black Level (0-100 percent)" initialValue="0" onChangeFunc={onChangeFunc}></PivConfigField>
                <PivConfigField fieldname="cameragain" fieldTitle="Gain (0-47 dB)" initialValue="0" onChangeFunc={onChangeFunc}></PivConfigField>
                <PivConfigField fieldname="cameragamma" fieldTitle="Gamma (0.5-2.0)" initialValue="1" onChangeFunc={onChangeFunc}></PivConfigField>
              </div>
            </fieldset>
          </div>

          <div className="configurationgroup">
            <fieldset style={{ border: '1px solid #ccc', padding: '1px', width: '99%', justifyContent: 'center' }}>
              <legend style={{ padding: '0 10px' }}>Timing</legend>
              <div className="configurationrow">
                <PivConfigField fieldname="shutteropentime" fieldTitle="Shutter time (ms)" initialValue="20" onChangeFunc={onChangeFunc}></PivConfigField>
                <PivConfigField fieldname="laserontime" fieldTitle="Laser time (ms)" initialValue="20" onChangeFunc={onChangeFunc}></PivConfigField>
              </div>
              <div className="configurationrow">
                <PivConfigField fieldname="imagecount" fieldTitle="Number of frames in group" initialValue="2" onChangeFunc={onChangeFunc}></PivConfigField>
                <PivConfigField fieldname="imagerate" fieldTitle="Frame repeat period (ms)" initialValue="20" onChangeFunc={onChangeFunc}></PivConfigField>
              </div>
              <div className="configurationrow">
                <PivConfigField fieldname="framerate" fieldTitle="Group Repeat period (ms)" initialValue="50" onChangeFunc={onChangeFunc}></PivConfigField>
                <PivConfigField fieldname="framecount" fieldTitle="Total group count" initialValue="0" onChangeFunc={onChangeFunc}></PivConfigField>
              </div>
            </fieldset>
          </div>

          <div className="configurationgroup">
            <fieldset style={{ border: '1px solid #ccc', padding: '1px', width: '99%', justifyContent: 'center' }}>
              <legend style={{ padding: '0 10px' }}>Status</legend>
              <div className="configurationrow">
                <PivProgressField fieldname="progress" fieldTitle="Progress" initialValue=""></PivProgressField>
                <PivUpdateField fieldname="timeremaining" fieldTitle="Seconds" initialValue=""></PivUpdateField>
                <PivUpdateField fieldname="iteration" fieldTitle="Count" initialValue=""></PivUpdateField>
                <PivStatusLed fieldname="startingled" fieldTitle="Execution Starting" value={deploying}></PivStatusLed>
                <PivStatusLed fieldname="runningled" fieldTitle="Execution Running" value={deployrunning}></PivStatusLed>
              </div>
            </fieldset>
          </div>
  
        </div>
    )
}

export default PivConfigBoxNormal;
