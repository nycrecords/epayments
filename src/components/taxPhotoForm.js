import React from 'react';
import {Grid, Form} from 'semantic-ui-react';

class TaxPhotoForm extends React.Component {
     constructor() {
         super();
         this.state = {
             block: '',
             lot: '',
             row: '',
             borough: '',
             buildingNum: '',
             street: '',
             mail: false,
             contactNum: '',
             comment: '',
             addDescription: '',
             collection: '',
             printSize: ''
         }
     }
    render() {
        return (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Group inline>
                            <label>Collection</label>
                            <Form.Radio
                                name="collection"
                                label='1940'
                                checked={this.state.collection === "1940"}
                                onChange={(e) => {
                                    this.setState({collection: "1940"})
                                    this.props.callBack("collection", "1940", this.props.index, this.props.state.collection)
                                }}

                            />
                            <Form.Radio
                                name="collection"
                                label='1980'
                                checked={this.state.collection === "1980"}
                                onChange={(e) => {
                                    this.setState({collection: "1980"})
                                    this.props.callBack("collection", "1980", this.props.index, this.props.state.collection)
                                }}
                            />
                            <Form.Radio
                                name="collection"
                                label='Both'
                                checked={this.state.collection === "Both"}
                                onChange={(e) => {
                                    this.setState({collection: "Both"})
                                    this.props.callBack("collection", "Both", this.props.index, this.props.state.collection)
                                }}
                            />
                        </Form.Group>

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
                        <Form.Input label="Roll"
                                    name="roll"
                                    placeholder="Roll#"
                                    onChange={(e, {value}) => {
                                        this.setState({roll: e.target.value})
                                        this.props.callBack("roll", value, this.props.index, this.props.state.roll)
                                    }}
                                    value={this.state.roll}
                        />
                        <Form.Group inline>
                            <label>Printing Size</label>

                            <Form.Radio
                                name={"printSize"}
                                label='8" x 10" Print'
                                checked={this.state.printSize === '8x10'}
                                onChange={(e) => {
                                    this.setState({printSize: '8x10'})
                                    this.props.callBack("printSize", '8x10', this.props.index, this.props.state.printSize);
                                }}
                            />

                            <Form.Radio
                                name={"printSize"}
                                label='11" x 14" Print'
                                checked={this.state.printSize === '11x14'}
                                onChange={(e) => {
                                    this.setState({printSize: '11x14'})
                                    this.props.callBack("printSize", '11x14', this.props.index, this.props.state.printSize);
                                }}
                            />
                        </Form.Group>
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
                                               this.props.callBack("mail", true, this.props.index, this.props.state.mail) :
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
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
    }
}

export default TaxPhotoForm;