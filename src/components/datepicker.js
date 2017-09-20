/**
 * Created by sinsang on 4/26/17.
 */
import React from 'react';
import DatePicker from 'react-datepicker';
import moment from 'moment';
import 'react-datepicker/dist/react-datepicker.css';
import MaskedInput from 'react-text-mask';
import {Form} from 'semantic-ui-react';
import PropTypes from 'prop-types';

class Input extends React.Component {  // !!! Must be a class; DatePicker gives its customInput prop a ref
  render() {
    const {onChange, onClick, value, label, inputName} = this.props;

    return (
      <Form.Input
        required
        label={label}
        name={name}
        children={
          <MaskedInput
            mask={[/\d/, /\d/, '/', /\d/, /\d/, '/', /\d/, /\d/, /\d/, /\d/]}
            placeholder="MM/DD/YYYY"
            name={inputName}
            required
            pattern="(0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])[- /.]\d\d\d\d"
            value={value}
            onChange={onChange}
            onClick={onClick}
          />
        }
      />
    )
  }
}
class Date extends React.Component {
    static propTypes = {
    label: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    maxDate: PropTypes.object
  };

  state = {
    date: undefined,
    moment: this.props.maxDate || null,
  };


  handleChange = (date) => {
    this.setState({
      date: date,
    });
  };

  handleChangeRaw = (e) => {
    const value = e.target.value;
    // update the date value if the format is valid, even though the date itself might be wrong
      this.setState({
        date: moment(value, "MM/DD/YYYY")
      })
  };

  render() {
    const {date, moment} = this.state;
    const {label, name} = this.props;

    return <DatePicker
      maxDate={moment}
      selected={date}
      customInput={
        <Input
          onChange={this.handleChange}
          label={label}
          inputName={name}
        />
      }
      onChange={this.handleChange}
      onChangeRaw={this.handleChangeRaw}
    />;
  }

}

export default Date