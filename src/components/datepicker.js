/**
 * Created by sinsang on 4/26/17.
 */
import React from 'react';
import DatePicker from 'react-datepicker';
import moment from 'moment';
import 'react-datepicker/dist/react-datepicker.css';


class Date extends React.Component {
    constructor (props) {
        super(props);
        this.state = {
            date_received: moment(),
            date_submitted: moment()
        };
        this.handleChange = this.handleChange.bind(this);
        fetch('api/v1.0/orders', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                date_received: this.state.date_received,
                date_submitted: this.state.date_submitted,
            })
        })
    }

    handleChange(date) {
        this.setState({
            date_received: date,
            date_submitted: date
        });

        console.log(date);
    }
    handleDate(date) {
        this.setState({date: date._d})
    };


    render() {
        return <DatePicker
            placeholderText={this.state.date_received}
            todayButton="Today"
            selected={this.state.date_submitted}
            // selected={}
            onChange={this.handleChange}

        />;
    }

}

export default Date