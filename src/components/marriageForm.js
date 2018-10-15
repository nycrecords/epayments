import React from 'react';
import {Form, Grid} from 'semantic-ui-react';
import {dayOptions, monthOptions} from "../constants/constants";

class MarriageForm extends React.Component {
    constructor() {
        super();

        this.state = {
            certificateNum: '',
            groomLastName: '',
            groomFirstName: '',
            brideLastName: '',
            brideFirstName: '',
            month: '',
            day: '',
            years: [
                {label: 'Year', name: 'year', value: ''},
                {label: 'Year 2', name: 'year2', value: ''}
            ],
            marriagePlace: '',
            boroughs: [
                {label: 'Manhattan', name: 'manhattan', checked: false},
                {label: 'Brooklyn', name: 'brooklyn', checked: false},
                {label: 'Bronx', name: 'bronx', checked: false},
                {label: 'Queens', name: 'queens', checked: false},
                {label: 'Staten Island', name: 'statenIsland', checked: false}
            ],
            comment: '',
            letter: false,
            deliveryMethod: ''
        }
    }

    handleChange = (e) => {
        this.setState({
            [e.target.name]: e.target.value
        });
        this.props.handleFormChange(e.target.name, e.target.value);
    };

    handleSelectChange = (e, data) => {
        this.setState({
            [data.name]: data.value
        });
        this.props.handleFormChange(data.name, data.value);
    };

    handleYearChange = (index, e) => {
        let newYears = this.state.years.slice();
        newYears[index].value = e.target.value;
        this.setState({
            years: newYears
        });
        this.props.handleFormChange('years', this.state.years);
    };

    handleBoroughChange = (index, e) => {
        let newBoroughs = this.state.boroughs.slice();
        newBoroughs[index].checked = !newBoroughs[index].checked;
        this.setState({
            boroughs: newBoroughs
        });
        this.props.handleFormChange('boroughs', this.state.boroughs);
    };

    handleLetterChange = () => {
        this.setState({
            letter: !this.state.letter
        }, () =>
        this.props.handleFormChange('letter', this.state.letter));
    };

    handleRadioChange = (e, {name, value}) => {
        let stateName = name.replace(/\d+/g, '');
        this.setState({
            [stateName]: value
        });
        this.props.handleFormChange(stateName, value);
    };

    render() {
        return (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Input label="Certificate Number (if known)"
                                    name="certificateNum"
                                    placeholder="Certificate Number"
                                    maxLength={40}
                                    onChange={this.handleChange}
                                    value={this.state.certificateNum}
                        />
                        <Form.Input label="Last Name of Bride/Groom/Spouse 1"
                                    name="groomLastName"
                                    placeholder="Groom Last Name"
                                    maxLength={25}
                                    required
                                    onChange={this.handleChange}
                                    value={this.state.groomLastName}
                        />
                        <Form.Input label="First Name of Bride/Groom/Spouse 1"
                                    name="groomFirstName"
                                    placeholder="Groom First Name"
                                    maxLength={40}
                                    onChange={this.handleChange}
                                    value={this.state.groomFirstName}
                        />
                        <Form.Input label="Last Name of Bride/Groom/Spouse 2"
                                    name="brideLastName"
                                    placeholder="Bride Last Name"
                                    maxLength={25}
                                    required
                                    onChange={this.handleChange}
                                    value={this.state.brideLastName}
                        />
                        <Form.Input label="First Name of Bride/Groom/Spouse 2"
                                    name="brideFirstName"
                                    placeholder="Bride First Name"
                                    maxLength={40}
                                    onChange={this.handleChange}
                                    value={this.state.brideFirstName}
                        />

                        <p><strong>Date of Marriage</strong></p>
                        <Form.Group>
                            <Form.Select label="Month"
                                         name="month"
                                         placeholder="Month"
                                         width={3}
                                         options={monthOptions}
                                         onChange={this.handleSelectChange}
                                         value={this.state.month}
                            />
                            <Form.Select label="Day"
                                         name="day"
                                         placeholder="Day"
                                         width={3}
                                         options={dayOptions}
                                         onChange={this.handleSelectChange}
                                         value={this.state.day}
                            />
                            <Form.Input label="Year"
                                        name="year"
                                        maxLength={4}
                                        placeholder="Year"
                                        required
                                        onChange={(e, {value}) => {
                                            if (/^[0-9]+$/.test(value.slice(-1)) || value === '') {
                                                this.handleYearChange(0, e);
                                            }
                                        }}
                                        value={this.state.year}
                            />
                        </Form.Group>

                        <p><strong>Additional Years to Search</strong></p>
                        {/* Use reduce to start map from second index since first index is used above */}
                        {this.state.years.reduce((mappedArray, year, index) => {
                                if (index > 0) {
                                    mappedArray.push(<Form.Input key={index}
                                                                 label={year.label}
                                                                 name={year.name}
                                                                 maxLength={4}
                                                                 value={year.value}
                                                                 onChange={this.handleYearChange.bind(this, index)}
                                    />);
                                }
                                return mappedArray;
                            }, []
                        )}

                        <Form.Input label="Place of Marriage"
                                    name="marriagePlace"
                                    placeholder="Marriage Place"
                                    maxLength={40}
                                    onChange={this.handleChange}
                                    value={this.state.marriagePlace}
                        />

                        <p className='required-label'><strong>Borough/County</strong></p>
                        {this.state.boroughs.map((borough, i) =>
                            <Form.Checkbox key={i}
                                           label={borough.label}
                                           name={borough.name}
                                           onChange={this.handleBoroughChange.bind(this, i)}
                            />
                        )}

                        <Form.Input label="Comment"
                                    name="comment"
                                    placeholder="Comment"
                                    maxLength={255}
                                    onChange={this.handleChange}
                                    value={this.state.comment}
                        />

                        <Form.Checkbox label='Attach "Letter of Exemplification"'
                                       name="letter"
                                       className="letterField"
                                       onChange={this.handleLetterChange}
                        />

                        <Form.Group grouped>
                            <label className='required-label'>Delivery Method</label>
                            <Form.Radio
                                label='Mail'
                                name={'deliveryMethod' + this.props.suborderKey}
                                value='mail'
                                checked={this.state.deliveryMethod === "mail"}
                                onChange={this.handleRadioChange}

                            />
                            <Form.Radio
                                label='Email'
                                name={'deliveryMethod' + this.props.suborderKey}
                                value='email'
                                checked={this.state.deliveryMethod === "email"}
                                onChange={this.handleRadioChange}
                            />
                        </Form.Group>
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
    }
}

export {MarriageForm};
