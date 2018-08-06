import React from 'react'
import {Grid, Form} from 'semantic-ui-react';
class PropertyCardForm extends React.Component {
     constructor() {
         super();
         this.state = {
             certified: '',
             block: '',
             lot: '',
             borough: '',
             buildingNum: '',
             street: '',
             mail: false,
             contactNum: '',
             imgId: '',
             imgTitle: '',
             comment: '',
             personalUseAgreement: false,
             addDescription: '',
             printSize: '',
         }
     }
    render() {
        return (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Input label="Block"
                                    name="block"
                                    placeholder="Block"
                                    onChange={(e, {value}) => {
                                        this.setState({block: value})
                                        this.props.callBack("block", value, this.props.index, this.props.state.block)
                                    }}
                                    value={this.state.block}
                        />
                        <Form.Input label="Lot"
                                    name="lot"
                                    placeholder="Lot"
                                    onChange={(e, {value}) => {
                                        this.setState({lot: value})
                                        this.props.callBack("lot", value, this.props.index, this.props.state.lot)
                                    }}
                                    value={this.state.lot}
                        />
                        <Form.Select label="Borough"
                                     required
                                     name="borough"
                                     options={this.props.boroughOptions}
                                     placeholder="Borough"
                                     onChange={(e, {value}) => {
                                         this.setState({borough: value});
                                         this.props.callBack("borough", value, this.props.index, this.props.state.borough);

                                     }}
                                     value={this.state.value}
                        />
                        <Form.Input label="Building Number"
                                    name="buildingNum"
                                    placeholder="Building Number"
                                    onChange={(e, {value}) => {
                                        this.setState({buildingNum: value})
                                        this.props.callBack("buildingNum", value, this.props.index, this.props.state.buildingNum)
                                    }}
                                    value={this.state.buildingNum}
                        />
                        <Form.Input label="Street"
                                    name="street"
                                    placeholder="Street"
                                    onChange={(e, {value}) => {
                                        this.setState({street: value})
                                        this.props.callBack("street", value, this.props.index, this.props.state.street)
                                    }}
                                    value={this.state.street}
                        />
                        <Form.Checkbox label="Mail"
                                       name="mail"
                                       onChange={() => {
                                           (this.state.mail === false) ?
                                               this.props.callBack("mail", true, this.props.index, this.props.state.mail):
                                               this.props.callBack("mail", false, this.props.index, this.props.state.mail);
                                           (this.state.mail === false) ?
                                               this.setState({mail: true}) :
                                               this.setState({mail: false})
                                       }}
                        />
                        <Form.Input label="description"
                                    name="addDescription"
                                    placeholder="Description"
                                    onChange={(e, {value}) => {
                                        this.setState({addDescription: value})
                                        this.props.callBack("addDescription", value, this.props.index, this.props.state.addDescription)
                                    }}
                                    value={this.state.addDescription}
                        />
                        <Form.Input label="Contact Number"
                                    name="contactNum"
                                    placeholder="Contact Number"
                                    onChange={(e, {value}) => {
                                        this.setState({contactNum: value})
                                        this.props.callBack("contactNum", value, this.props.index, this.props.state.contactNum)
                                    }}
                                    value={this.state.contactNum}
                        />
                        <Form.Input label="Certified"
                                    name="certified"
                                    placeholder="Certified"
                                    onChange={(e, {value}) => {
                                        this.setState({certified: value})
                                        this.props.callBack("certified", value, this.props.index, this.props.state.certified)
                                    }}
                                    value={this.state.certified}
                        />
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
    }
}

export default PropertyCardForm;