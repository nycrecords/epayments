import React from 'react';
import {Grid, Form} from 'semantic-ui-react';

class VitalRecordForm extends React.Component {

    render() {
        return (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Input label="Month"
                                    name="month"
                                    placeholder="Month"
                                    maxLength={20}
                                    onChange={(e, {value}) => {
                                        this.props.callBack("month", value, this.props.index, this.props.state.suborder.month)

                                    }}
                                    value={this.props.state.suborder.month[this.props.index]}
                        />
                        <Form.Input label="Day"
                                    name="day"
                                    maxLength={2}
                                    placeholder="Day"
                                    onChange={(e, {value}) => {
                                        if (/^[0-9]+$/.test(value.slice(-1)) || value === '') {
                                            this.props.callBack("day", value, this.props.index, this.props.state.suborder.day)
                                        }
                                    }}
                                    value={this.props.state.suborder.day[this.props.index]}
                        />
                        <Form.Input label="Year"
                                    name="year"
                                    maxLength={4}
                                    required
                                    placeholder="Year"
                                    onChange={(e, {value}) => {
                                        if (/^[0-9]+$/.test(value.slice(-1)) || value === '') {
                                            this.props.callBack("year", value, this.props.index, this.props.state.suborder.year)
                                        }
                                    }}
                                    value={this.props.state.suborder.year[this.props.index]}
                        />
                        <Form.Select label="Borough"
                                     required
                                     name="borough"
                                     options={this.props.boroughOptions}
                                     placeholder="Borough"
                                     onChange={(e, {value}) => {
                                         this.props.callBack("borough", value, this.props.index, this.props.state.suborder.borough);

                                     }}
                                     value={this.props.state.suborder.borough[this.props.index]}
                        />
                        <Form.Checkbox label="Letter"
                                       name="letter"
                                       onChange={() => {
                                           (this.props.state.suborder.letter[this.props.index] === false) ?
                                               this.props.callBack("letter", true, this.props.index, this.props.state.suborder.letter) :
                                               this.props.callBack("letter", false, this.props.index, this.props.state.suborder.letter);
                                       }}
                        />
                        <Form.Input label="Comment"
                                    name="comment"
                                    placeholder="Comment"
                                    maxLength={255}
                                    onChange={(e, {value}) => {
                                        this.props.callBack("comment", value, this.props.index, this.props.state.suborder.comment)
                                    }}
                                    value={this.props.state.suborder.comment[this.props.index]}
                        />

                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
    }
}

export default VitalRecordForm;