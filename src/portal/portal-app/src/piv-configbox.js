import './App.css';
import PivConfigBoxNormal from './piv-configbox-normal';
import PivConfigBoxTest from './piv-configbox-test';

const PivConfigBox = ({deploying, deployrunning, onChangeFunc, pingdata, test}) => {
    return (
      <>
        {test ? <PivConfigBoxTest pingdata={pingdata} onChangeFunc={onChangeFunc}/> : <PivConfigBoxNormal deploying={deploying} deployrunning={deployrunning} onChangeFunc={onChangeFunc}/>}
      </>
    );
}

export default PivConfigBox;
