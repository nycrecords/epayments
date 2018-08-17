import React from 'react';
import {Grid, Form} from 'semantic-ui-react';
import VitalRecordForm from "./vitalRecordForm";

class MarriageSearchForm extends React.Component {

    render() {
        return (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Group>
                            <Form.Input label="Groom First Name"
                                        name="groomFirstName"
                                        placeholder="Groom First Name"
                                        maxLength={40}
                                        onChange={(e, {value}) => {
                                            this.props.callBack("groomFirstName", value, this.props.index, this.props.state.suborder.groomFirstName)
                                        }}
                                        value={this.props.state.suborder.groomFirstName[this.props.index]}
                            />
                            <Form.Input label="Groom Last Name"
                                        name="groomLastName"
                                        placeholder="Groom Last Name"
                                        maxLength={25}
                                        onChange={(e, {value}) => {
                                            this.props.callBack("groomLastName", value, this.props.index, this.props.state.suborder.groomLastName)
                                        }}
                                        value={this.props.state.suborder.groomLastName[this.props.index]}
                            />
                        </Form.Group>
                        <Form.Group>
                            <Form.Input label="Bride First Name"
                                        name="brideFirstName"
                                        placeholder="Bride First Name"
                                        maxLength={40}
                                        onChange={(e, {value}) => {
                                            this.props.callBack("brideFirstName", value, this.props.index, this.props.state.suborder.brideFirstName)
                                        }}
                                        value={this.props.state.suborder.brideFirstName[this.props.index]}
                            />
                            <Form.Input label="Bride Last Name"
                                        name="brideLastName"
                                        placeholder="Bride Last Name"
                                        maxLength={25}
                                        onChange={(e, {value}) => {
                                            this.props.callBack("brideLastName", value, this.props.index, this.props.state.suborder.brideLastName)
                                        }}
                                        value={this.props.state.suborder.brideLastName[this.props.index]}
                            />
                        </Form.Group>
                        <Form.Input label="Marriage Place"
                                    name="marriagePlace"
                                    placeholder="Marriage Place"
                                    maxLength={40}
                                    onChange={(e, {value}) => {
                                        this.props.callBack("marriagePlace", value, this.props.index, this.props.state.suborder.marriagePlace)
                                    }}
                                    value={this.props.state.suborder.marriagePlace[this.props.index]}
                        />
                        <VitalRecordForm callBack={this.props.callBack} index={this.props.index}
                                         state={this.props.state} boroughOptions={this.props.boroughOptions}/>
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
    }
}

class MarriageCertForm extends React.Component {

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
                        <MarriageSearchForm callBack={this.props.callBack} index={this.props.index}
                                            state={this.props.state} boroughOptions={this.props.boroughOptions}/>

                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
    }
}

export {MarriageSearchForm, MarriageCertForm};