import './App.css';
import PivConfigField from './piv-configfield';
import SonarPingData from './sonar-pingdata';


const PivConfigBoxTest = ({pingdata, connectionstyle, setconnectionstyle, onChangeFunc}) => {
  return (
        <div className="configurationbox">
          <div className="configurationgroup">
            Step Command
            <div className="configurationrow">
              <PivConfigField fieldname="range" fieldTitle="Range (1-200m) inc=1" initialValue="1" onChangeFunc={onChangeFunc}></PivConfigField>
              <PivConfigField fieldname="gain" fieldTitle="Gain (0-40db) inc=1" initialValue="30" onChangeFunc={onChangeFunc}></PivConfigField>
              <PivConfigField fieldname="logf" fieldTitle="Logf (10, 20, 30, 40db)" initialValue="20" onChangeFunc={onChangeFunc}></PivConfigField>
              <PivConfigField fieldname="absorption" fieldTitle="Absorption (0.00-2.55db) inc=0.01" initialValue="0.60" onChangeFunc={onChangeFunc}></PivConfigField>
            </div>
            <div className="configurationrow">
              <PivConfigField fieldname="sector_width" fieldTitle="Sector Width (0-360deg) inc=3" initialValue="0" onChangeFunc={onChangeFunc}></PivConfigField>
              <PivConfigField fieldname="train_angle" fieldTitle="Train Angle (-180-180deg) inc=3" initialValue="0" onChangeFunc={onChangeFunc}></PivConfigField>
              <PivConfigField fieldname="step_size" fieldTitle="Step Size (0-2.4deg) inc 0.3" initialValue="1.2" onChangeFunc={onChangeFunc}></PivConfigField>
              <PivConfigField fieldname="calibrate" fieldTitle="Calibrate (0, 1)" initialValue="0" onChangeFunc={onChangeFunc}></PivConfigField>
            </div>
            <div className="configurationrow">
              <PivConfigField fieldname="pulse_length" fieldTitle="Pulse Length (10-1000us) inc=10" initialValue="200" onChangeFunc={onChangeFunc}></PivConfigField>
              <PivConfigField fieldname="data_points" fieldTitle="Data Points (250, 500)" initialValue="500" onChangeFunc={onChangeFunc}></PivConfigField>
              <PivConfigField fieldname="profile" fieldTitle="Profile (0, 1)" initialValue="0" onChangeFunc={onChangeFunc}></PivConfigField>
              <PivConfigField fieldname="frequency" fieldTitle="Frequency (175-1175kHz) inc=5" initialValue="1000" onChangeFunc={onChangeFunc}></PivConfigField>
            </div>
          </div>

          <div className="configurationgroup">
            Step Response
            <div className="configurationrow">
              <PivConfigField fieldname="resp_header" fieldTitle="Header" initialValue="" onChangeFunc={onChangeFunc}></PivConfigField>
              <PivConfigField fieldname="resp_headid" fieldTitle="Head ID" initialValue="0" onChangeFunc={onChangeFunc}></PivConfigField>
            </div>
            <div className="configurationrow">
              <PivConfigField fieldname="resp_serial_V5" fieldTitle="Firmware" initialValue="" onChangeFunc={onChangeFunc}></PivConfigField>
              <PivConfigField fieldname="resp_serial_switches" fieldTitle="Switches Accepted" initialValue="1" onChangeFunc={onChangeFunc}></PivConfigField>
              <PivConfigField fieldname="resp_serial_overrun" fieldTitle="Serial Overrun" initialValue="0" onChangeFunc={onChangeFunc}></PivConfigField>
              <PivConfigField fieldname="resp_headpos" fieldTitle="Head Position" initialValue="30" onChangeFunc={onChangeFunc}></PivConfigField>
            </div>
            <div className="configurationrow">
              <PivConfigField fieldname="resp_headrange" fieldTitle="Head Range" initialValue="1" onChangeFunc={onChangeFunc}></PivConfigField>
              <PivConfigField fieldname="resp_profilerange" fieldTitle="Profile Range" initialValue="4" onChangeFunc={onChangeFunc}></PivConfigField>
              <PivConfigField fieldname="resp_bytecount" fieldTitle="Byte Count" initialValue="4" onChangeFunc={onChangeFunc}></PivConfigField>
              <PivConfigField fieldname="resp_brightness" fieldTitle="Brightness" initialValue="4" onChangeFunc={onChangeFunc}></PivConfigField>
            </div>
          </div>
          <SonarPingData pingdata={pingdata} />
        </div>
    )
}

export default PivConfigBoxTest;
