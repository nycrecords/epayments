import React from 'react';
import {Grid, Form} from 'semantic-ui-react';
import VitalRecordForm from "./vitalRecordForm";

class BirthSearchForm extends React.Component {

    render() {
        return (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Input label="First Name"
                                    name="firstName"
                                    placeholder="First Name"
                                    maxLength={40}
                                    onChange={(e, {value}) => {
                                        this.props.callBack("firstName", value, this.props.index, this.props.state.suborder.firstName)
                                    }}
                                    value={this.props.state.suborder.firstName[this.props.index]}
                        />
                        <Form.Input label="Middle Name"
                                    name="middleName"
                                    placeholder="Middle Name"
                                    maxLength={40}
                                    onChange={(e, {value}) => {
                                        this.props.callBack("middleName", value, this.props.index, this.props.state.suborder.middleName)
                                    }}
                                    value={this.props.state.suborder.middleName[this.props.index]}
                        />
                        <Form.Input label="Last Name"
                                    name="lastName"
                                    placeholder="Last Name"
                                    maxLength={25}
                                    onChange={(e, {value}) => {
                                        this.props.callBack("lastName", value, this.props.index, this.props.state.suborder.lastName)
                                    }}
                                    value={this.props.state.suborder.lastName[this.props.index]}
                        />
                        <Form.Input label="Birth Place"
                                    name="birthPlace"
                                    placeholder="BirthPlace"
                                    maxLength={40}
                                    onChange={(e, {value}) => {
                                        this.props.callBack("birthPlace", value, this.props.index, this.props.state.suborder.birthPlace)
                                    }}
                                    value={this.props.state.suborder.birthPlace[this.props.index]}
                        />
                        <Form.Select label="Gender"
                                     required
                                     name="gender"
                                     placeholder="Gender"
                                     options={this.props.genderOptions}
                                     onChange={(e, {value}) => {
                                         this.props.callBack("gender", value, this.props.index, this.props.state.suborder.gender);
                                     }}
                                     value={this.props.state.suborder.gender[this.props.index]}
                        />
                        <Form.Input label="Mother Name"
                                    name="motherName"
                                    placeholder="Mother Name"
                                    maxLength={40}
                                    onChange={(e, {value}) => {
                                        this.props.callBack("motherName", value, this.props.index, this.props.state.suborder.motherName)
                                    }}
                                    value={this.props.state.suborder.motherName[this.props.index]}
                        />
                        <Form.Input label="Father Name"
                                    name="fatherName"
                                    placeholder="Father Name"
                                    maxLength={40}
                                    onChange={(e, {value}) => {
                                        this.props.callBack("fatherName", value, this.props.index, this.props.state.suborder.fatherName)
                                    }}
                                    value={this.props.state.suborder.fatherName[this.props.index]}
                        />
                        <VitalRecordForm callBack={this.props.callBack} index={this.props.index}
                                         state={this.props.state} boroughOptions={this.props.boroughOptions}/>
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
    }
}

class BirthCertForm extends React.Component {

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
                                        this.props.callBack("certificateNum", value, this.props.index, this.props.state.suborder.certificateNum)
                                    }}
                                    value={this.props.state.suborder.certificateNum[this.props.index]}
                        />
                        <BirthSearchForm callBack={this.props.callBack} index={this.props.index}
                                         state={this.props.state} boroughOptions={this.props.boroughOptions}
                                         genderOptions={this.props.genderOptions}/>
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
    }
}

export {BirthSearchForm, BirthCertForm};