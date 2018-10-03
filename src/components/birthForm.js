import React from 'react';
import {Form, Grid} from 'semantic-ui-react';
import {dayOptions, genderOptions, monthOptions} from '../constants/constants';

class BirthForm extends React.Component {
    constructor() {
        super();

        this.state = {
            certificateNum: '',
            gender: '',
            lastName: '',
            firstName: '',
            middleName: '',
            month: '',
            day: '',
            years: [
                {label: 'Year', name: 'year', value: ''},
                {label: 'Year 2', name: 'year2', value: ''},
                {label: 'Year 3', name: 'year3', value: ''},
                {label: 'Year 4', name: 'year4', value: ''},
                {label: 'Year 5', name: 'year5', value: ''}
            ],
            birthPlace: '',
            boroughs: [
                {label: 'Manhattan', name: 'manhattan', checked: false},
                {label: 'Brooklyn', name: 'brooklyn', checked: false},
                {label: 'Bronx', name: 'bronx', checked: false},
                {label: 'Queens', name: 'queens', checked: false},
                {label: 'Staten Island', name: 'statenIsland', checked: false}
            ],
            fatherName: '',
            motherName: '',
            comment: '',
            letter: false,
            deliveryMethod: ''
        };
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
        console.log(this.state.boroughs);
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
                        <Form.Select label="Gender"
                                     name="gender"
                                     placeholder="Gender"
                                     options={genderOptions}
                                     onChange={this.handleSelectChange}
                                     value={this.state.gender}
                        />
                        <Form.Input label="Last Name"
                                    name="lastName"
                                    placeholder="Last Name"
                                    maxLength={25}
                                    required
                                    onChange={this.handleChange}
                                    value={this.state.lastName}
                        />
                        <Form.Input label="First Name"
                                    name="firstName"
                                    placeholder="First Name"
                                    maxLength={40}
                                    onChange={this.handleChange}
                                    value={this.state.firstName}
                        />
                        <Form.Input label="Middle Name"
                                    name="middleName"
                                    placeholder="Middle Name"
                                    maxLength={40}
                                    onChange={this.handleChange}
                                    value={this.state.middleName}
                        />

                        <p><strong>Date of Birth</strong></p>
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

                        <Form.Input label="Place of birth"
                                    name="birthPlace"
                                    placeholder="Birth Place"
                                    maxLength={40}
                                    onChange={this.handleChange}
                                    value={this.state.birthPlace}
                        />

                        <p><strong>BOROUGH/COUNTY Available</strong></p>
                        {this.state.boroughs.map((borough, i) =>
                            <Form.Checkbox key={i}
                                           label={borough.label}
                                           name={borough.name}
                                           onChange={this.handleBoroughChange.bind(this, i)}
                            />
                        )}

                        <Form.Input label="Father's Name"
                                    name="fatherName"
                                    placeholder="Father's Name"
                                    maxLength={40}
                                    onChange={this.handleChange}
                                    value={this.state.fatherName}
                        />
                        <Form.Input label="Mother's Name"
                                    name="motherName"
                                    placeholder="Mother's Name"
                                    maxLength={40}
                                    onChange={this.handleChange}
                                    value={this.state.motherName}
                        />
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
                            <label>Delivery Method</label>
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

export {BirthForm};