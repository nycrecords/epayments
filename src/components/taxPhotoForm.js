import React from 'react';
import {Grid, Form} from 'semantic-ui-react';

class TaxPhotoForm extends React.Component {

    render() {
        return (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Group inline>
                            <label>Collection</label>
                            <Form.Radio
                                label='1940'
                                checked={this.props.state.suborder.collection[this.props.index] === "1940"}
                                onChange={(e) => {
                                    this.props.callBack("collection", "1940", this.props.index, this.props.state.suborder.collection)
                                }}

                            />
                            <Form.Radio
                                label='1980'
                                checked={this.props.state.suborder.collection[this.props.index] === "1980"}
                                onChange={(e) => {
                                    this.props.callBack("collection", "1980", this.props.index, this.props.state.suborder.collection)
                                }}
                            />
                            <Form.Radio
                                label='Both'
                                checked={this.props.state.suborder.collection[this.props.index] === "Both"}
                                onChange={(e) => {
                                    this.props.callBack("collection", "Both", this.props.index, this.props.state.suborder.collection)
                                }}
                            />
                        </Form.Group>

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
                        <Form.Input label="Roll"
                                    name="roll"
                                    placeholder="Roll#"
                                    maxLength={9}
                                    onChange={(e, {value}) => {
                                        this.props.callBack("roll", value, this.props.index, this.props.state.suborder.roll)
                                    }}
                                    value={this.props.state.suborder.roll[this.props.index]}
                        />
                        <Form.Group inline>
                            <label>Printing Size</label>

                            <Form.Radio
                                label='8" x 10" Print'
                                checked={this.props.state.suborder.printSize[this.props.index] === '8x10'}
                                onChange={(e) => {
                                    this.props.callBack("printSize", '8x10', this.props.index, this.props.state.suborder.printSize);
                                }}
                            />

                            <Form.Radio
                                label='11" x 14" Print'
                                checked={this.props.state.suborder.printSize[this.props.index] === '11x14'}
                                onChange={(e) => {
                                    this.props.callBack("printSize", '11x14', this.props.index, this.props.state.suborder.printSize);
                                }}
                            />
                        </Form.Group>
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
                                    placeholder="Building Number"
                                    maxLength={10}
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
                                       checked={this.props.state.suborder.mail[this.props.index]}
                        />
                        <Form.Input label="Description"
                                    name="addDescription"
                                    placeholder="Description"
                                    maxLength={35}
                                    onChange={(e, {value}) => {
                                        this.props.callBack("addDescription", value, this.props.index, this.props.state.suborder.addDescription)
                                    }}
                                    value={this.props.state.suborder.addDescription[this.props.index]}
                        />
                        <Form.Input label="Contact Number"
                                    name="contactNum"
                                    placeholder="Contact Number"
                                    maxLength={10}
                                    onChange={(e, {value}) => {
                                        this.props.callBack("contactNum", value, this.props.index, this.props.state.suborder.contactNum)
                                    }}
                                    value={this.props.state.suborder.contactNum[this.props.index]}
                        />
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
    }
}

export default TaxPhotoForm;