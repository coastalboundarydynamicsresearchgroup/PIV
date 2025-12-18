import './App.css';
import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';
import PivDatasets from './piv-datasets';


const PivConfigButtons = ({deploying, deployrunning, getStateFunc, onCreateFunc, onSaveFunc, onDeleteFunc, OnExecuteFunc, onDownloadFunc, onTestFunc}) => {

  const GetSelectedConfiguration = () => {
    var selectedConfiguration = -1;
    const configurationsSelectList = document.getElementById("configurationsselectlist");
    if (configurationsSelectList) {
      selectedConfiguration = configurationsSelectList.selectedIndex;
    }

    return selectedConfiguration;
  }

  const CreateButtonEnabled = () => {
    return getStateFunc('nametouched');
  }

  const SaveButtonEnabled = () => {
    return GetSelectedConfiguration() >= 0 && !getStateFunc('nametouched') && getStateFunc('valuetouched');
  }

  const DeleteButtonEnabled = () => {
    return GetSelectedConfiguration() >= 0 && !getStateFunc('nametouched');
  }

  const ExecuteAndTestButtonEnabled = () => {
    return GetSelectedConfiguration() >= 0 && !getStateFunc('nametouched') && !getStateFunc('valuetouched');
  }

  const ExecuteButtonText = () => {
    const deployFlag = !deploying && !deployrunning;
    return deployFlag ? "Execute" : "Stop";
  }

  const TestButtonText = () => {
    const deployFlag = !deploying && !deployrunning;
    return deployFlag ? "Test" : "Stop";
  }

  var configurations =  ['10ms', '100ms', '1s', '10s', '1min', '10min', '1hour', '1day'];

  return (
    <div className="configuration-buttons">
      <div className="configuration-buttonrow">
        <button type="button" id="create-button" disabled={!CreateButtonEnabled()} onClick={onCreateFunc}>
            Create
        </button>

        <button type="button" id="save-button" disabled={!SaveButtonEnabled()} onClick={onSaveFunc}>
            Save
        </button>
      </div>

      <div className="configuration-buttonrow">
        <button type="button" id="delete-button" disabled={!DeleteButtonEnabled()} onClick={onDeleteFunc}>
            Delete
        </button>
      </div>

      <div className="configuration-buttonrow">
        <button type="button" id="deploy-button" disabled={!ExecuteAndTestButtonEnabled()} onClick={OnExecuteFunc}>
            { ExecuteButtonText() }
        </button>
        <button type="button" id="test-button" disabled={!ExecuteAndTestButtonEnabled()} onClick={onTestFunc}>
            { TestButtonText() }
        </button>
      </div>

      <div className="configuration-buttonrow">
        <Popup trigger={
          <button type="button" id="download-button" onClick={onDownloadFunc}>
              Manage Datasets...
          </button>}
          position = "top center" >
          <PivDatasets />
        </Popup>
      </div>

     </div>
  );
}

export default PivConfigButtons;

