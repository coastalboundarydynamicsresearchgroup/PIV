import './App.css';

const PivCheckBox = ({fieldname, fieldTitle, initialValue, onChangeFunc}) => {

    return (
      <div className="configurationcheckbox">
        <input id={fieldname} type="checkbox" value={initialValue} onChange={onChangeFunc}></input>
        <label htmlFor={fieldname}>{fieldTitle}</label>
      </div>
    )
}

export default PivCheckBox;
