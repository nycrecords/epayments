import React, {} from 'react';

class PhotoGalleryForm extends React.Component {
    render() {
        return (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Input label="Image Identifier"
                                    name="imgId"
                                    placeholder="Image Identifier"
                                    onChange={this.handleChange}
                                    value={this.state.imgId}
                        />

                        <Form.Input label="Title/Description of Image"
                                    name="imgTitle"
                                    placeholder="Title/Description of Image"
                                    onChange={this.handleChange}
                                    value={this.state.imgTitle}
                        />

                        <Form.Input label="Addition Description"
                                    name="addDescription"
                                    placeholder="Addition Description"
                                    onChange={this.handleChange}
                                    value={this.state.addDescription}
                        />
                        <Form.Checkbox label="Mail"
                                       name="mail"
                                       onChange={() => {
                                           (this.state.mail == false) ?
                                               this.setState({mail: true}) &&
                                               this.props.callBack("mail", true) :
                                               this.setState({mail: false}) &&
                                               this.props.callBack("mail", true);
                                       }}
                                       value={this.state.mail}
                        />
                        <Form.Input label="Contact Number"
                                    name="contactNum"
                                    placeholder="Contact Number"
                                    onChange={this.handleChange}
                                    value={this.state.contactNum}
                        />
                        <Form.Checkbox label="Personal Use Agreement"
                                       name="personalUseAgreement"
                                       onChange={() => {
                                           (this.state.personalUseAgreement == false) ?
                                               this.setState({personalUseAgreement: true}) &&
                                               this.props.callBack("personalUseAgreement", true) :
                                               this.setState({personalUseAgreement: false}) &&
                                               this.props.callBack("personalUseAgreement", true);
                                       }}
                                       value={this.state.personalUseAgreement}
                        />
                        <Form.Input label="Comment"
                                    name="comment"
                                    placeholder="Comment"
                                    onChange={this.handleChange}
                                    value={this.state.comment}
                        />
                        <Form.Group inline required>
                            <label>Printing Size</label>

                            <Form.Radio
                                name={"printSize"}
                                label='8" x 10" Print'
                                checked={this.state.printSize === '8x10'}
                                onChange={(e, {}) => {
                                    this.setState({printSize: '8x10'})
                                    this.props.callBack("printSize", '8x10');
                                }}
                            />

                            <Form.Radio
                                name={"printSize"}
                                label='11" x 14" Print'
                                checked={this.state.printSize === '11x14'}
                                onChange={(e, {}) => {
                                    this.setState({printSize: '11x14'})
                                    this.props.callBack("printSize", '11x14');
                                }}
                            />

                            <Form.Radio
                                name={"printSize"}
                                label='16" x 20" Print'
                                checked={this.state.printSize === '16x20'}
                                onChange={(e, {}) => {
                                    this.setState({printSize: '16x20'})
                                    this.props.callBack("printSize", '16x20');
                                }}
                            />

                        </Form.Group>
                    </Grid.Column>
                </Grid.Row>
            </Grid>


    )
    }
}

export default PhotoGalleryForm;