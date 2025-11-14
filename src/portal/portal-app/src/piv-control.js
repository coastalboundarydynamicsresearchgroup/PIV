import { useState, useEffect } from 'react';
import PivConfigure from './piv-configure';
import PivConfigBox from './piv-configbox';
import PivProgressPollerSingleton from './piv-progresspoller';
import './App.css';

const PivControl = () => {
    const [configNameTouched, setConfigNameTouched] = useState(false);
    const [configValueTouched, setConfigValueTouched] = useState(false);
    const [test, setTest] = useState(false);
    const [testdata, setTestdata] = useState("");
    const [connectionStyle, setConnectionStyle] = useState("flir");

    const [deploying, setDeploying] = useState(false);
    const [deployrunning, setDeployrunning] = useState(false);

    const handleProgressUpdate = (progress) => {
      console.log(progress);

      const progressfield = document.getElementById('progress');
      if (progressfield) {
        if (progress.status) {
          progressfield.value = progress.status;
        }
      }

      const timeremainingfield = document.getElementById('timeremaining');
      if (timeremainingfield) {
        if (progress.delaySec != null) {
          timeremainingfield.value = progress.delaySec;
        }
      }

      const iterationfield = document.getElementById('iteration');
      if (iterationfield) {
        if (progress.count != null) {
          iterationfield.value = progress.count;
        }
      }

      const startingledfield = document.getElementById('startingled');
      if (startingledfield) {
        if (progress.deploying != null) {
          startingledfield.value = progress.deploying;
          setDeploying(progress.deploying);
        }
      }

      const runningledfield = document.getElementById('runningled');
      if (runningledfield) {
        if (progress.deployrunning != null) {
          runningledfield.value = progress.deployrunning;
          setDeployrunning(progress.deployrunning);
        }
      }
    }

    useEffect(() => {
      PivProgressPollerSingleton.getInstance(handleProgressUpdate);
    }, []);

    const getState = (stateName) => {
        switch(stateName)
        {
            case 'nametouched':
                return configNameTouched;
            case 'valuetouched':
                return configValueTouched;
            default:
                return false;
        }
    }

    const setState = (stateName, value) => {
        switch(stateName)
        {
            case 'nametouched':
                setConfigNameTouched(value);
                break;
            case 'valuetouched':
                setConfigValueTouched(value);
                break;
            default:
                break;
        }
    }

    const onTestClicked = () => {
      if (test) {
          setTest(false);
      } else {
          setTest(true);
      }
    }

    const onPivTestData = (testreturndata) => {
        console.log(`Setting state variable with test data ${testreturndata}`);
        setTestdata(testreturndata);
    }

    return (
        <section className="fullpane">
        <div className="connectbar">
            <div className="titleLabel">PIV Configuration and Control</div>

            <div className="messagebar">
            <div className="messages">
                <div className="configurationsLabel">Select a configuration, edit, and deploy</div>
                <div className="configurations">
                    <PivConfigure getState={getState} setState={setState} deploying={deploying} deployrunning={deployrunning} onTestClicked={onTestClicked} onPingData={onPivTestData} test={test} connectionstyle={connectionStyle} setconnectionstyle={setConnectionStyle} />
                    <PivConfigBox  onChangeFunc={() => setState('valuetouched', true)} deploying={deploying} deployrunning={deployrunning} pingdata={testdata} test={test} connectionstyle={connectionStyle} setconnectionstyle={setConnectionStyle} />
                </div>
                <textarea name="messages" id="messages" cols="120" rows="8" readOnly></textarea>
                <textarea name="status" id="status" cols="120" rows="5" readOnly></textarea>
            </div>
            </div>

        </div>
        </section>
    );
}

export default PivControl;
