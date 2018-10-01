import React from 'react';
import {Grid, Form} from 'semantic-ui-react';

class TaxPhotoForm extends React.Component {
    constructor() {
        super();
        this.state = {
            collection: '',
            borough: '',
            buildingNum: '',
            street: '',
            description: '',
            block: '',
            lot: '',
            roll: '',
            size: '',
            letter: false,
            deliveryMethod: '',
            contactNum: '',
        }
    }

    handleChange = (e) => {
        this.setState({
            [e.target.name]: e.target.value
        });
        this.props.handleFormChange(e.target.name, e.target.value);
    };

    handleRadioChange = (e, {name, value}) => {
        this.setState({
            [name]: value
        });
        this.props.handleFormChange(name, value);
    };

    render() {
        return (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Group grouped>
                            <label>Collection</label>
                            <Form.Radio
                                label='1940'
                                name='collection'
                                value='1940'
                                checked={this.state.collection === "1940"}
                                onChange={this.handleRadioChange}

                            />
                            <Form.Radio
                                label='1980'
                                name='collection'
                                value='1980'
                                checked={this.state.collection === "1980"}
                                onChange={this.handleRadioChange}
                            />
                            <Form.Radio
                                label='Both'
                                name='collection'
                                value='Both'
                                checked={this.state.collection === "Both"}
                                onChange={this.handleRadioChange}
                            />
                        </Form.Group>

                        <Form.Group grouped>
                            <label>Borough</label>
                            <Form.Radio
                                label='Brooklyn'
                                name='borough'
                                value='Brooklyn'
                                checked={this.state.borough === "Brooklyn"}
                                onChange={this.handleRadioChange}

                            />
                            <Form.Radio
                                label='Manhattan'
                                name='borough'
                                value='Manhattan'
                                checked={this.state.borough === "Manhattan"}
                                onChange={this.handleRadioChange}
                            />
                            <Form.Radio
                                label='Queens'
                                name='borough'
                                value='Queens'
                                checked={this.state.borough === "Queens"}
                                onChange={this.handleRadioChange}
                            />
                            <Form.Radio
                                label='Staten Island'
                                name='borough'
                                value='Staten Island'
                                checked={this.state.borough === "Staten Island"}
                                onChange={this.handleRadioChange}
                            />
                            <Form.Radio
                                label='Bronx'
                                name='borough'
                                value='Bronx'
                                checked={this.state.borough === "Bronx"}
                                onChange={this.handleRadioChange}
                            />
                        </Form.Group>

                        <Form.Input label="Building Number"
                                    name="buildingNum"
                                    placeholder="Building Number"
                                    maxLength={10}
                                    required
                                    onChange={this.handleChange}
                                    value={this.state.buildingNum}
                        />
                        <Form.Input label="Street Name"
                                    name="street"
                                    placeholder="Street"
                                    maxLength={40}
                                    onChange={this.handleChange}
                                    value={this.state.street}
                        />
                        <Form.Input label="Description"
                                    name="description"
                                    placeholder="Description"
                                    maxLength={35}
                                    onChange={this.handleChange}
                                    value={this.state.description}
                        />

                        <p><strong>Block & Lot Information</strong></p>
                        <Form.Input label="Block"
                                    name="block"
                                    placeholder="Block"
                                    maxLength={9}
                                    onChange={this.handleChange}
                                    value={this.state.block}
                        />
                        <Form.Input label="Lot"
                                    name="lot"
                                    placeholder="Lot"
                                    maxLength={9}
                                    onChange={this.handleChange}
                                    value={this.state.lot}
                        />
                        <Form.Input label="Roll# (1940s Only)"
                                    name="roll"
                                    placeholder="Roll"
                                    maxLength={9}
                                    onChange={this.handleChange}
                                    value={this.state.roll}
                        />

                        <p><strong>Print Information</strong></p>
                        <Form.Group grouped>
                            <label>Collection</label>
                            <Form.Radio
                                label='8" x 10" Print'
                                name='size'
                                value='8x10'
                                checked={this.state.size === "8x10"}
                                onChange={this.handleRadioChange}

                            />
                            <Form.Radio
                                label='11" x 14" Print'
                                name='size'
                                value='11x14'
                                checked={this.state.size === "11x14"}
                                onChange={this.handleRadioChange}
                            />
                        </Form.Group>

                        <Form.Group grouped>
                            <label>Delivery Method</label>
                            <Form.Radio
                                label='Mail'
                                name='deliveryMethod'
                                value='mail'
                                checked={this.state.deliveryMethod === "mail"}
                                onChange={this.handleRadioChange}

                            />
                            <Form.Radio
                                label='Email'
                                name='deliveryMethod'
                                value='email'
                                checked={this.state.deliveryMethod === "email"}
                                onChange={this.handleRadioChange}
                            />
                            <Form.Radio
                                label='Pickup'
                                name='deliveryMethod'
                                value='pickup'
                                checked={this.state.deliveryMethod === "pickup"}
                                onChange={this.handleRadioChange}
                            />
                            {this.state.deliveryMethod === "pickup" && <Form.Input label="Contact Number"
                                                                                   name="contactNum"
                                                                                   placeholder="Contact Number"
                                                                                   maxLength={10}
                                                                                   onChange={this.handleChange}
                                                                                   value={this.state.contactNum}
                            />}
                        </Form.Group>
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
    }
}

export default TaxPhotoForm;