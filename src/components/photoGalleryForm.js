import React, {} from 'react';
import {Grid, Form} from 'semantic-ui-react';

class PhotoGalleryForm extends React.Component {

    render() {
        return (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Input label="Image Identifier"
                                    name="imgId"
                                    placeholder="Image Identifier"
                                    maxLength={20}
                                    onChange={(e, {value}) => {
                                        this.props.callBack("imgId", value, this.props.index, this.props.state.imgId)
                                    }}
                                    value={this.props.state.imgId[this.props.index]}
                        />

                        <Form.Input label="Title/Description of Image"
                                    name="imgTitle"
                                    maxLength={500}
                                    placeholder="Title/Description of Image"
                                    onChange={(e, {value}) => {
                                        this.props.callBack("imgTitle", value, this.props.index, this.props.state.imgTitle)
                                    }}
                                    value={this.props.state.imgTitle[this.props.index]}
                        />

                        <Form.Input label="Addition Description"
                                    name="addDescription"
                                    placeholder="Addition Description"
                                    maxLength={500}
                                    onChange={(e, {value}) => {
                                        this.props.callBack("addDescription", value, this.props.index, this.props.state.addDescription)
                                    }}
                                    value={this.props.state.addDescription[this.props.index]}
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
                        <Form.Input label="Contact Number"
                                    name="contactNum"
                                    placeholder="Contact Number"
                                    maxLength={10}
                                    onChange={(e, {value}) => {
                                        this.props.callBack("contactNum", value, this.props.index, this.props.state.contactNum)
                                    }}
                                    value={this.props.state.contactNum[this.props.index]}
                        />
                        <Form.Checkbox label="Personal Use Agreement"
                                       name="personalUseAgreement"
                                       onChange={() => {
                                           (this.props.state.personalUseAgreement[this.props.index] === false) ?
                                               this.props.callBack("personalUseAgreement", true, this.props.index, this.props.state.personalUseAgreement) :
                                               this.props.callBack("personalUseAgreement", false, this.props.index, this.props.state.personalUseAgreement);
                                       }}
                                       checked={this.props.state.personalUseAgreement[this.props.index]}
                        />
                        <Form.Input label="Comment"
                                    name="comment"
                                    placeholder="Comment"
                                    maxLength={255}
                                    onChange={(e, {value}) => {
                                        this.props.callBack("comment", value, this.props.index, this.props.state.comment)
                                    }}
                                    value={this.props.state.comment[this.props.index]}
                        />
                        <Form.Group inline required>
                            <label>Printing Size</label>

                            <Form.Radio
                                label='8" x 10" Print'
                                checked={this.props.state.printSize[this.props.index] === '8x10'}
                                onChange={(e) => {
                                    this.props.callBack("printSize", '8x10', this.props.index, this.props.state.printSize);
                                }}
                            />

                            <Form.Radio
                                label='11" x 14" Print'
                                checked={this.props.state.printSize[this.props.index] === '11x14'}
                                onChange={(e) => {
                                    this.props.callBack("printSize", '11x14', this.props.index, this.props.state.printSize);
                                }}
                            />

                            <Form.Radio
                                label='16" x 20" Print'
                                checked={this.props.state.printSize[this.props.index] === '16x20'}
                                onChange={(e) => {
                                    this.props.callBack("printSize", '16x20', this.props.index, this.props.state.printSize);
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