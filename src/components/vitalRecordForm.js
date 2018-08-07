import React from 'react';
import {Grid, Form} from 'semantic-ui-react';

class VitalRecordForm extends React.Component {
    constructor() {
        super()
        this.state = {
            month: '',
            day: '',
            year: '',
            letter: false,
            borough: '',
            comment: ''
        }
    }

    render() {
        return (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Group>
                            <Form.Input label="Month"
                                        name="month"
                                        placeholder="Month"
                                        onChange={(e, {value}) => {

                                            this.setState({month: value})
                                            this.props.callBack("month", value, this.props.index, this.props.state.month)

                                        }}
                                        value={this.props.state.month[this.props.index]}
                            />
                            <Form.Input label="Day"
                                        name="day"
                                        maxLength={2}
                                        placeholder="Day"
                                        onChange={(e, {value}) => {
                                            if (/^[0-9]+$/.test(value.slice(-1)) || value === '') {
                                                this.setState({day: value})
                                                this.props.callBack("day", value, this.props.index, this.props.state.day)
                                            }
                                        }}
                                        value={this.props.state.day[this.props.index]}
                            />
                            <Form.Input label="Year"
                                        name="year"
                                        maxLength={4}
                                        placeholder="Year"
                                        onChange={(e, {value}) => {
                                            if (/^[0-9]+$/.test(value.slice(-1)) || value === '') {
                                                this.setState({year: value})
                                                this.props.callBack("year", value, this.props.index, this.props.state.year)
                                            }
                                        }}
                                        value={this.props.state.year[this.props.index]}
                            />
                        </Form.Group>

                        <Form.Select label="Borough"
                                     required
                                     name="borough"
                                     options={this.props.boroughOptions}
                                     placeholder="Borough"
                                     onChange={(e, {value}) => {
                                         this.setState({borough: value});
                                         this.props.callBack("borough", value, this.props.index, this.props.state.borough);

                                     }}
                                     value={this.props.state.borough[this.props.index]}
                        />
                        <Form.Checkbox label="Letter"
                                       name="letter"
                                       onChange={() => {
                                           (this.state.letter === false) ?
                                               this.props.callBack("letter", true, this.props.index, this.props.state.letter) :
                                               this.props.callBack("letter", false, this.props.index, this.props.state.letter);
                                           (this.state.letter === false) ?
                                               this.setState({letter: true}) :
                                               this.setState({letter: false});
                                       }}
                        />
                        <Form.Input label="Comment"
                                    name="comment"
                                    placeholder="Comment"
                                    onChange={(e, {value}) => {
                                        this.setState({comment: value})
                                        this.props.callBack("comment", value, this.props.index, this.props.state.comment)
                                    }}
                                    value={this.props.state.comment[this.props.index]}
                        />

                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
    }
}

export default VitalRecordForm;