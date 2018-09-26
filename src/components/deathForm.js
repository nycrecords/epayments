import React from 'react';
import {Grid, Form} from 'semantic-ui-react';
import VitalRecordForm from "./vitalRecordForm";

class DeathForm extends React.Component {
    constructor() {
        super();

        this.state = {
            certificateNum: '',
            cemetery: '',
            lastName: '',
            firstName: '',
            middleName: '',
            deathPlace: '',
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
                        <Form.Input label="Cemetery"
                                    name="cemetery"
                                    placeholder="Cemetery"
                                    maxLength={40}
                                    onChange={this.handleChange}
                                    value={this.state.cemetery}
                        />
                        <Form.Input label="Death Place"
                                    name="deathPlace"
                                    placeholder="Death Place"
                                    maxLength={40}
                                    onChange={this.handleChange}
                                    value={this.state.deathPlace}
                        />
                        <VitalRecordForm callBack={this.props.callBack} index={this.props.index}
                                         state={this.props.state} boroughOptions={this.props.boroughOptions}/>
                    </Grid.Column>
                </Grid.Row>
            </Grid>

        )
    }
}

class DeathCertForm extends React.Component {
    constructor() {
        super();
        this.state = {
            cemetery: '',
            lastName: '',
            firstName: '',
            middleName: '',
            deathPlace: '',
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
                        {/*<DeathSearchForm callBack={this.props.callBack} index={this.props.index}*/}
                                         {/*state={this.props.state} boroughOptions={this.props.boroughOptions}/>*/}
                    </Grid.Column>
                </Grid.Row>
            </Grid>

        )
    }
}

export {DeathForm};

