import React from 'react'
import {Grid, Form} from 'semantic-ui-react';

class PropertyCardForm extends React.Component {

    render() {
        return (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Input label="Block"
                                    name="block"
                                    placeholder="Block"
                                    maxLength={9}
                                    onChange={(e, {value}) => {
                                        this.props.callBack("block", value, this.props.index, this.props.state.block)
                                    }}
                                    value={this.props.state.block[this.props.index]}
                        />
                        <Form.Input label="Lot"
                                    name="lot"
                                    placeholder="Lot"
                                    maxLength={9}
                                    onChange={(e, {value}) => {
                                        this.props.callBack("lot", value, this.props.index, this.props.state.lot)
                                    }}
                                    value={this.props.state.lot[this.props.index]}
                        />
                        <Form.Select label="Borough"
                                     required
                                     name="borough"
                                     options={this.props.boroughOptions}
                                     placeholder="Borough"
                                     onChange={(e, {value}) => {
                                         this.props.callBack("borough", value, this.props.index, this.props.state.borough);

                                     }}
                                     value={this.props.state.borough[this.props.index]}
                        />
                        <Form.Input label="Building Number"
                                    name="buildingNum"
                                    maxLength={10}
                                    placeholder="Building Number"
                                    onChange={(e, {value}) => {
                                        this.props.callBack("buildingNum", value, this.props.index, this.props.state.buildingNum)
                                    }}
                                    value={this.props.state.buildingNum[this.props.index]}
                        />
                        <Form.Input label="Street"
                                    name="street"
                                    placeholder="Street"
                                    maxLength={40}
                                    onChange={(e, {value}) => {
                                        this.props.callBack("street", value, this.props.index, this.props.state.street)
                                    }}
                                    value={this.props.state.street[this.props.index]}
                        />
                        <Form.Checkbox label="Mail"
                                       name="mail"
                                       onChange={() => {
                                           (this.props.state.mail[this.props.index] === false) ?
                                               this.props.callBack("mail", true, this.props.index, this.props.state.mail) :
                                               this.props.callBack("mail", false, this.props.index, this.props.state.mail);
                                       }}
                                       checked={this.props.state.mail[this.props.index]}
                        />
                        <Form.Input label="description"
                                    name="addDescription"
                                    placeholder="Description"
                                    maxLength={40}
                                    onChange={(e, {value}) => {
                                        this.props.callBack("addDescription", value, this.props.index, this.props.state.addDescription)
                                    }}
                                    value={this.props.state.addDescription[this.props.index]}
                        />
                        <Form.Input label="Contact Number"
                                    name="contactNum"
                                    placeholder="Contact Number"
                                    maxLength={35}
                                    onChange={(e, {value}) => {
                                        this.props.callBack("contactNum", value, this.props.index, this.props.state.contactNum)
                                    }}
                                    value={this.props.state.contactNum[this.props.index]}
                        />
                        <Form.Input label="Certified"
                                    name="certified"
                                    placeholder="Certified"
                                    maxLength={40}
                                    onChange={(e, {value}) => {
                                        this.props.callBack("certified", value, this.props.index, this.props.state.certified)
                                    }}
                                    value={this.props.state.certified[this.props.index]}
                        />
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
    }
}

export default PropertyCardForm;