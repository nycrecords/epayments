import React from 'react';
import {Grid, Form} from 'semantic-ui-react';
import VitalRecordForm from "./vitalRecordForm";

class MarriageSearchForm extends React.Component {
    constructor() {
        super();

        this.state = {
            certificateNum: '',
            groomLastName: '',
            groomFirstName: '',
            brideLastName: '',
            brideFirstName: '',
            marriagePlace: '',
        }
    }

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
                                            this.setState({groomFirstName: value})
                                            this.props.callBack("groomFirstName", value, this.props.index, this.props.state.groomFirstName)
                                        }}
                                        value={this.state.groomFirstName}
                            />
                            <Form.Input label="Groom Last Name"
                                        name="groomLastName"
                                        placeholder="Groom Last Name"
                                        maxLength={25}
                                        onChange={(e, {value}) => {
                                            this.setState({groomLastName: value})
                                            this.props.callBack("groomLastName", value, this.props.index, this.props.state.groomLastName)
                                        }}
                                        value={this.state.groomLastName}
                            />
                        </Form.Group>
                        <Form.Group>
                            <Form.Input label="Bride First Name"
                                        name="brideFirstName"
                                        placeholder="Bride First Name"
                                        maxLength={40}
                                        onChange={(e, {value}) => {
                                            this.setState({brideFirstName: value})
                                            this.props.callBack("brideFirstName", value, this.props.index, this.props.state.brideFirstName)
                                        }}
                                        value={this.state.brideFirstName}
                            />
                            <Form.Input label="Bride Last Name"
                                        name="brideLastName"
                                        placeholder="Bride Last Name"
                                        maxLength={25}
                                        onChange={(e, {value}) => {
                                            this.setState({brideLastName: value})
                                            this.props.callBack("brideLastName", value, this.props.index, this.props.state.brideLastName)
                                        }}
                                        value={this.state.brideLastName}
                            />
                        </Form.Group>
                        <Form.Input label="Marriage Place"
                                    name="marriagePlace"
                                    placeholder="Marriage Place"
                                    maxLength={40}
                                    onChange={(e, {value}) => {
                                        this.setState({marriagePlace: value})
                                        this.props.callBack("marriagePlace", value, this.props.index, this.props.state.marriagePlace)
                                    }}
                                    value={this.state.marriagePlace}
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
    constructor() {
        super()
        this.state = {
            certificateNum: '',
            groomLastName: '',
            groomFirstName: '',
            brideLastName: '',
            brideFirstName: '',
            marriagePlace: '',

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
                        <MarriageSearchForm callBack={this.props.callBack} index={this.props.index}
                                            state={this.props.state} boroughOptions={this.props.boroughOptions}/>

                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
    }
}

export {MarriageSearchForm, MarriageCertForm};