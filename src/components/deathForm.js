import React from 'react';
import {Grid, Form} from 'semantic-ui-react';
import VitalRecordForm from "./vitalRecordForm";

class DeathSearchForm extends React.Component {
    constructor() {
        super()
        this.state = {
            cemetery: '',
            lastName: '',
            firstName: '',
            middleName: '',
            deathPlace: '',
        }
    }
    render() {
        return (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        {/*<Form.Group>*/}
                            <Form.Input label="First Name"
                                        name="firstName"
                                        placeholder="First Name"
                                        maxLength={40}
                                        onChange={(e, {value}) => {
                                            this.setState({firstName: value})
                                            this.props.callBack("firstName", value, this.props.index, this.props.state.firstName)
                                        }}
                                        value={this.props.state.firstName[this.props.index]}
                            />
                            <Form.Input label="Middle Name"
                                        name="middleName"
                                        placeholder="Middle Name"
                                        maxLength={40}
                                        onChange={(e, {value}) => {
                                            this.setState({middleName: value})
                                            this.props.callBack("middleName", value, this.props.index, this.props.state.middleName)
                                        }}
                                        value={this.props.state.middleName[this.props.index]}
                            />
                            <Form.Input label="Last Name"
                                        name="lastName"
                                        placeholder="Last Name"
                                        maxLength={25}
                                        onChange={(e, {value}) => {
                                            this.setState({lastName: value})
                                            this.props.callBack("lastName", value, this.props.index, this.props.state.lastName)
                                        }}
                                        value={this.props.state.lastName[this.props.index]}
                            />
                        {/*</Form.Group>*/}
                        <Form.Input label="Cemetery"
                                    name="cemetery"
                                    placeholder="Cemetery"
                                    maxLength={40}
                                    onChange={(e, {value}) => {
                                        this.setState({cemetery: value})
                                        this.props.callBack("cemetery", value, this.props.index, this.props.state.cemetery)
                                    }}
                                    value={this.props.state.cemetery[this.props.index]}
                        />
                        <Form.Input label="Death Place"
                                    name="deathPlace"
                                    placeholder="Death Place"
                                    maxLength={40}
                                    onChange={(e, {value}) => {
                                        this.setState({deathPlace: value})
                                        this.props.callBack("deathPlace", value, this.props.index, this.props.state.deathPlace)
                                    }}
                                    value={this.props.state.deathPlace[this.props.index]}
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
        super()
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
                                        this.setState({certificateNum: value})
                                        this.props.callBack("certificateNum", value, this.props.index, this.props.state.certificateNum)
                                    }}
                                    value={this.props.state.certificateNum[this.props.index]}
                        />
                        <DeathSearchForm callBack={this.props.callBack} index={this.props.index}
                                         state={this.props.state} boroughOptions={this.props.boroughOptions}/>
                    </Grid.Column>
                </Grid.Row>
            </Grid>

        )
    }
}

export {DeathCertForm, DeathSearchForm};

