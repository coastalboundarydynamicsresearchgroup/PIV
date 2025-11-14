function PivRadioGroup({ options, name, onChange, selectedValue, setselectedValue}) {
  const handleChange = (event) => {
    const value = event.target.value;
    setselectedValue(value);
    onChange(value);
  };

  return (
    <fieldset style={{ border: '1px solid #ccc', padding: '10px', width: '20%' }}>
      <legend style={{ padding: '0 10px' }}>Connection Style:</legend>
      {options.map((option) => (
        <label key={option.value}>
          <input
            type="radio"
            name={name}
            value={option.value}
            checked={selectedValue === option.value}
            onChange={handleChange}
          />
          {option.label}
        </label>
      ))}
    </fieldset>
  );
}

export default PivRadioGroup;
