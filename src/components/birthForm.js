import React from 'react';
import {Grid, Form} from 'semantic-ui-react';
import VitalRecordForm from "./vitalRecordForm";
import {boroughOptions, genderOptions} from '../constants/constants';

class BirthSearchForm extends React.Component {
    constructor() {
        super();

        this.state = {
            certificateNum: '',
            gender: '',
            fatherName: '',
            motherName: '',
            birthPlace: '',
            lastName: '',
            firstName: '',
            middleName: '',
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
                        <Form.Input label="Last Name"
                                    name="lastName"
                                    placeholder="Last Name"
                                    maxLength={25}
                                    onChange={this.handleChange}
                                    value={this.state.lastName}
                        />
                        <Form.Input label="Birth Place"
                                    name="birthPlace"
                                    placeholder="BirthPlace"
                                    maxLength={40}
                                    onChange={this.handleChange}
                                    value={this.state.birthPlace}
                        />
                        <Form.Select label="Gender"
                                     required
                                     name="gender"
                                     placeholder="Gender"
                                     options={genderOptions}
                                     onChange={this.handleSelectChange}
                                     value={this.state.gender}
                        />
                        <Form.Input label="Mother Name"
                                    name="motherName"
                                    placeholder="Mother Name"
                                    maxLength={40}
                                    onChange={this.handleChange}
                                    value={this.state.motherName}
                        />
                        <Form.Input label="Father Name"
                                    name="fatherName"
                                    placeholder="Father Name"
                                    maxLength={40}
                                    onChange={this.handleChange}
                                    value={this.state.fatherName}
                        />
                        <VitalRecordForm />
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
    }
}

class BirthCertForm extends React.Component {
    constructor() {
        super();

        this.state = {
            gender: '',
            fatherName: '',
            motherName: '',
            birthPlace: '',
            lastName: '',
            firstName: '',
            middleName: '',
            certificateNum: '',
        }
    }

    render() {
        return (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Input label="Certificate Number"
                                    name="certificateNum"
                                    placeholder="Certificate Number"
                                    maxLength={40}
                                    onChange={(e, {value}) => {
                                        this.setState({certificateNum: value});
                                        this.props.callBack("certificateNum", value, this.props.index, this.props.state.certificateNum)
                                    }}
                                    value={this.props.state.certificateNum[this.props.index]}
                        />
                        <BirthSearchForm callBack={this.props.callBack} index={this.props.index}
                                         state={this.props.state} boroughOptions={this.props.boroughOptions}
                                         genderOptions={genderOptions}/>
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
    }
}

export {BirthSearchForm, BirthCertForm};