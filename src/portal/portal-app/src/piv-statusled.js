import './App.css';

const PivStatusLed = ({fieldname, fieldTitle, value}) => {

    return (
      <div className="colordot">
        {fieldTitle}
        <span id={fieldname} className={value ? "greendot" : "greydot"}></span>
      </div>
    )
}

export default PivStatusLed;
