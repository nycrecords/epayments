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
                                        this.props.callBack("block", value, this.props.index, this.props.state.suborder.block)
                                    }}
                                    value={this.props.state.suborder.block[this.props.index]}
                        />
                        <Form.Input label="Lot"
                                    name="lot"
                                    placeholder="Lot"
                                    maxLength={9}
                                    onChange={(e, {value}) => {
                                        this.props.callBack("lot", value, this.props.index, this.props.state.suborder.lot)
                                    }}
                                    value={this.props.state.suborder.lot[this.props.index]}
                        />
                        <Form.Select label="Borough"
                                     required
                                     name="borough"
                                     options={this.props.boroughOptions}
                                     placeholder="Borough"
                                     onChange={(e, {value}) => {
                                         this.props.callBack("borough", value, this.props.index, this.props.state.suborder.borough);

                                     }}
                                     value={this.props.state.suborder.borough[this.props.index]}
                        />
                        <Form.Input label="Building Number"
                                    name="buildingNum"
                                    maxLength={10}
                                    placeholder="Building Number"
                                    onChange={(e, {value}) => {
                                        this.props.callBack("buildingNum", value, this.props.index, this.props.state.suborder.buildingNum)
                                    }}
                                    value={this.props.state.suborder.buildingNum[this.props.index]}
                        />
                        <Form.Input label="Street"
                                    name="street"
                                    placeholder="Street"
                                    maxLength={40}
                                    onChange={(e, {value}) => {
                                        this.props.callBack("street", value, this.props.index, this.props.state.suborder.street)
                                    }}
                                    value={this.props.state.suborder.street[this.props.index]}
                        />
                        <Form.Checkbox label="Mail"
                                       name="mail"
                                       onChange={() => {
                                           (this.props.state.suborder.mail[this.props.index] === false) ?
                                               this.props.callBack("mail", true, this.props.index, this.props.state.suborder.mail) :
                                               this.props.callBack("mail", false, this.props.index, this.props.state.suborder.mail);
                                       }}
                                       checked={this.props.state.mail[this.props.index]}
                        />
                        <Form.Input label="description"
                                    name="addDescription"
                                    placeholder="Description"
                                    maxLength={40}
                                    onChange={(e, {value}) => {
                                        this.props.callBack("addDescription", value, this.props.index, this.props.state.suborder.addDescription)
                                    }}
                                    value={this.props.state.suborder.addDescription[this.props.index]}
                        />
                        <Form.Input label="Contact Number"
                                    name="contactNum"
                                    placeholder="Contact Number"
                                    maxLength={35}
                                    onChange={(e, {value}) => {
                                        this.props.callBack("contactNum", value, this.props.index, this.props.state.suborder.contactNum)
                                    }}
                                    value={this.props.state.suborder.contactNum[this.props.index]}
                        />
                        <Form.Input label="Certified"
                                    name="certified"
                                    placeholder="Certified"
                                    maxLength={40}
                                    onChange={(e, {value}) => {
                                        this.props.callBack("certified", value, this.props.index, this.props.state.suborder.certified)
                                    }}
                                    value={this.props.state.suborder.certified[this.props.index]}
                        />
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
    }
}

export default PropertyCardForm;