import './App.css';
import PivConfigBoxNormal from './piv-configbox-normal';

const PivConfigBox = ({deploying, deployrunning, onChangeFunc}) => {
    return (
      <>
        {<PivConfigBoxNormal deploying={deploying} deployrunning={deployrunning} onChangeFunc={onChangeFunc}/>}
      </>
    );
}

export default PivConfigBox;
