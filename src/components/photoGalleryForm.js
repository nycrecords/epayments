import React, {} from 'react';
import {Grid, Form} from 'semantic-ui-react';


class PhotoGalleryForm extends React.Component {
     constructor() {
         super();
         this.state = {
             mail: false,
             contactNum: ' ',
             imgId: ' ',
             imgTitle: ' ',
             comment: ' ',
             personalUseAgreement: false,
             addDescription: ' ',
             printSize: ' ',
         }
     }
    render() {
        return (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Input label="Image Identifier"
                                    name="imgId"
                                    placeholder="Image Identifier"
                                    onChange={(e, {value}) => {
                                        this.setState({imgId: value})
                                        this.props.callBack("imgId", value, this.props.index, this.props.state.imgId)
                                    }}
                                    value={this.props.state.imgId[this.props.index]}
                        />

                        <Form.Input label="Title/Description of Image"
                                    name="imgTitle"
                                    placeholder="Title/Description of Image"
                                    onChange={(e, {value}) => {
                                        this.setState({imgTitle: value})
                                        this.props.callBack("imgTitle", value, this.props.index, this.props.state.imgTitle)
                                    }}
                                    value={this.props.state.imgTitle[this.props.index]}
                        />

                        <Form.Input label="Addition Description"
                                    name="addDescription"
                                    placeholder="Addition Description"
                                    onChange={(e, {value}) => {
                                        this.setState({addDescription: value})
                                        this.props.callBack("addDescription", value, this.props.index, this.props.state.addDescription)
                                    }}
                                    value={this.props.state.addDescription[this.props.index]}
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
                                       checked={this.props.state.mail[this.props.index]}
                        />
                        <Form.Input label="Contact Number"
                                    name="contactNum"
                                    placeholder="Contact Number"
                                    onChange={(e, {value}) => {
                                        this.setState({contactNum: value})
                                        this.props.callBack("contactNum", value, this.props.index, this.props.state.contactNum)
                                    }}
                                    value={this.props.state.contactNum[this.props.index]}
                        />
                        <Form.Checkbox label="Personal Use Agreement"
                                       name="personalUseAgreement"
                                       onChange={() => {
                                           (this.state.personalUseAgreement === false) ?
                                               this.props.callBack("personalUseAgreement", true, this.props.index, this.props.state.personalUseAgreement):
                                               this.props.callBack("personalUseAgreement", false, this.props.index, this.props.state.personalUseAgreement);
                                           (this.state.personalUseAgreement === false) ?
                                               this.setState({personalUseAgreement: true}) :
                                               this.setState({personalUseAgreement: false})
                                       }}
                                       checked={this.props.state.personalUseAgreement[this.props.index]}
                        />
                        <Form.Input label="Comment"
                                    name="comment"
                                    placeholder="Comment"
                                    onChange={(e, {value}) => {
                                        this.setState({comment: value})
                                        this.props.callBack("comment", value, this.props.index, this.props.state.comment)
                                    }}
                                    value={this.props.state.comment[this.props.index]}
                        />
                        <Form.Group inline required>
                            <label>Printing Size</label>

                            <Form.Radio
                                // name={"printSize"}
                                label='8" x 10" Print'
                                checked={this.props.state.printSize[this.props.index] === '8x10'}
                                onChange={(e) => {
                                    this.setState({printSize: '8x10'})
                                    this.props.callBack("printSize", '8x10', this.props.index, this.props.state.printSize);
                                }}
                            />

                            <Form.Radio
                                // name={"printSize"}
                                label='11" x 14" Print'
                                checked={this.props.state.printSize[this.props.index] === '11x14'}
                                onChange={(e) => {
                                    this.setState({printSize: '11x14'})
                                    this.props.callBack("printSize", '11x14', this.props.index, this.props.state.printSize);
                                }}
                            />

                            <Form.Radio
                                // name={"printSize"}
                                label='16" x 20" Print'
                                checked={this.props.state.printSize[this.props.index] === '16x20'}
                                onChange={(e) => {
                                    this.setState({printSize: '16x20'})
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