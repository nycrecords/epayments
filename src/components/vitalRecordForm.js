import React from 'react';
import {Grid, Form} from 'semantic-ui-react';
import {boroughOptions} from "../constants/constants";

class VitalRecordForm extends React.Component {
    constructor() {
        super();

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
                        {/*<Form.Group>*/}
                        <Form.Input label="Month"
                                    name="month"
                                    placeholder="Month"
                                    maxLength={20}
                                    onChange={(e, {value}) => {
                                        this.setState({month: value});
                                    }}
                                    value={this.state.month}
                        />
                        <Form.Input label="Day"
                                    name="day"
                                    maxLength={2}
                                    placeholder="Day"
                                    onChange={(e, {value}) => {
                                        if (/^[0-9]+$/.test(value.slice(-1)) || value === '') {
                                            this.setState({day: value});
                                        }
                                    }}
                                    value={this.state.day}
                        />
                        <Form.Input label="Year"
                                    name="year"
                                    maxLength={4}
                                    placeholder="Year"
                                    onChange={(e, {value}) => {
                                        if (/^[0-9]+$/.test(value.slice(-1)) || value === '') {
                                            this.setState({year: value});
                                        }
                                    }}
                                    value={this.state.year}
                        />
                        <Form.Select label="Borough"
                                     required
                                     name="borough"
                                     options={boroughOptions}
                                     placeholder="Borough"
                                     onChange={(e, {value}) => {
                                         this.setState({borough: value});
                                     }}
                                     value={this.state.borough}
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
                                    maxLength={255}
                                    onChange={(e, {value}) => {
                                        this.setState({comment: value});
                                    }}
                                    value={this.state.comment}
                        />

                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
    }
}

export default VitalRecordForm;