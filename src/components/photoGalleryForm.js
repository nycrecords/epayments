import React, {} from 'react';
import {Grid, Form} from 'semantic-ui-react';


class PhotoGalleryForm extends React.Component {
    constructor() {
        super();
        this.state = {
            imageID: '',
            description: '',
            additionalDescription: '',
            size: '',
            deliveryMethod: '',
            contactNum: '',
            comment: ''
        }
    }

    handleChange = (e) => {
        this.setState({
            [e.target.name]: e.target.value
        });
        this.props.handleFormChange(e.target.name, e.target.value);
    };

    handleRadioChange = (e, {name, value}) => {
        let stateName = name.replace(/\d+/g, '');
        this.setState({
            [stateName]: value
        });
        this.props.handleFormChange(stateName, value);
    };

    render() {
        return (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Input label="Image Identifier"
                                    name="imageID"
                                    placeholder="Image Identifier"
                                    maxLength={20}
                                    required
                                    onChange={this.handleChange}
                                    value={this.state.imageID}
                        />

                        <Form.Input label="Title/Description of Image"
                                    name="description"
                                    maxLength={150}
                                    placeholder="Title/Description of Image"
                                    onChange={this.handleChange}
                                    value={this.state.description}
                        />

                        <Form.Input label="Additional Description"
                                    name="additionalDescription"
                                    placeholder="Additional Description"
                                    maxLength={150}
                                    onChange={this.handleChange}
                                    value={this.props.additionalDescription}
                        />

                        <p><strong>Print Information</strong></p>
                        <Form.Group grouped>
                            <label className='required-label'>Size</label>
                            <Form.Radio
                                label='8" x 10" Print'
                                name={'size' + this.props.suborderKey}
                                value='8x10'
                                checked={this.state.size === "8x10"}
                                onChange={this.handleRadioChange}

                            />
                            <Form.Radio
                                label='11" x 14" Print'
                                name={'size' + this.props.suborderKey}
                                value='11x14'
                                checked={this.state.size === "11x14"}
                                onChange={this.handleRadioChange}
                            />
                            <Form.Radio
                                label='16" x 20" Print'
                                name={'size' + this.props.suborderKey}
                                value='11x14'
                                checked={this.state.size === "16x20"}
                                onChange={this.handleRadioChange}
                            />
                        </Form.Group>

                        <Form.Group grouped>
                            <label className='required-label'>Delivery Method</label>
                            <Form.Radio
                                label='Mail'
                                name={'deliveryMethod' + this.props.suborderKey}
                                value='mail'
                                checked={this.state.deliveryMethod === "mail"}
                                onChange={this.handleRadioChange}

                            />
                            <Form.Radio
                                label='Email'
                                name={'deliveryMethod' + this.props.suborderKey}
                                value='email'
                                checked={this.state.deliveryMethod === "email"}
                                onChange={this.handleRadioChange}
                            />
                            <Form.Radio
                                label='Pickup'
                                name={'deliveryMethod' + this.props.suborderKey}
                                value='pickup'
                                checked={this.state.deliveryMethod === "pickup"}
                                onChange={this.handleRadioChange}
                            />
                            {this.state.deliveryMethod === "pickup" && <Form.Input label="Contact Number"
                                                                                   name="contactNum"
                                                                                   placeholder="Contact Number"
                                                                                   maxLength={10}
                                                                                   required
                                                                                   onChange={this.handleChange}
                                                                                   value={this.state.contactNum}
                            />}
                        </Form.Group>

                        <Form.Input label="Comment"
                                    name="comment"
                                    placeholder="Comment"
                                    maxLength={255}
                                    onChange={this.handleChange}
                                    value={this.state.comment}
                        />
                    </Grid.Column>
                </Grid.Row>
            </Grid>


        )
    }
}

export default PhotoGalleryForm;