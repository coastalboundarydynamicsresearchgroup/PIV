import './App.css';
import PivConfigBoxNormal from './piv-configbox-normal';
import PivConfigBoxTest from './piv-configbox-test';

const PivConfigBox = ({deploying, deployrunning, onChangeFunc, pingdata, test, connectionstyle, setconnectionstyle}) => {
    return (
      <>
        {test ? <PivConfigBoxTest pingdata={pingdata} connectionstyle={connectionstyle} setconnectionstyle={setconnectionstyle} onChangeFunc={onChangeFunc}/> : <PivConfigBoxNormal deploying={deploying} deployrunning={deployrunning} connectionstyle={connectionstyle} setconnectionstyle={setconnectionstyle} onChangeFunc={onChangeFunc}/>}
      </>
    );
}

export default PivConfigBox;
