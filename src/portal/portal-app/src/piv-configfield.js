import './App.css';


const PivConfigField = ({fieldname, fieldTitle, initialValue, onChangeFunc}) => {

    return (
      <div className="configurationfield">
        {fieldTitle}
        <input id={fieldname} type="text" defaultValue={initialValue} onChange={onChangeFunc}></input>
      </div>
    )
}

export default PivConfigField;
