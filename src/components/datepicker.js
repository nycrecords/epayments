/**
 * Created by sinsang on 4/26/17.
 */
import React from 'react';
import DatePicker from 'react-datepicker';
import moment from 'moment';

import 'react-datepicker/dist/react-datepicker.css';

// CSS Modules, react-datepicker-cssmodules.css
// import 'react-datepicker/dist/react-datepicker-cssmodules.css';

class Date extends React.Component {
    constructor (props) {
        super(props);
        this.state = {
            startDate: moment()
        };
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(date) {
        this.setState({
            startDate: date
        });
    }

    render() {
        return <DatePicker
            placeholderText={this.state.startDate}
            todayButton="Today"
            selected={this.state.startDate}
            onChange={this.handleChange}
        />;
    }
}

export default Date