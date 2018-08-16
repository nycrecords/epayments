import React from 'react';
import {Button, Header, Modal, Form, TextArea} from 'semantic-ui-react';
import 'semantic-ui-css/semantic.min.css';
import {csrfFetch} from "../utils/fetch"
import swal from 'sweetalert';

class BatchStatusModal extends React.Component {
    constructor() {
        super();

        this.state = {
            modalOpen: false,
            comment: '',
            new_status: '',
            orders: []
        };
        this.handleOpen = (e) => this.setState({
            modalOpen: true,
        });

        this.handleClose = (e) => this.setState({
            modalOpen: false,
        });
        this.statuses = [
            {
                text: 'Received',
                value: 'Received',
            },
            {
                text: 'Processing',
                value: 'Processing',
            },
            {
                text: 'Found',
                value: 'Found',
            },
            {
                text: 'Printed',
                value: 'Printed',
            },
            {
                text: 'Mailed/Pickup',
                value: 'Mailed/Pickup',
            },
            {
                text: 'Not Found',
                value: 'Not_Found',
            },
            {
                text: 'Letter Generated',
                value: 'Letter_Generated',
            },
            {
                text: 'Undeliverable',
                value: 'Undeliverable',
            },
            {
                text: 'Refunded',
                value: 'Refunded',
            },
            {
                text: 'Done',
                value: 'Done',
            }

        ];

        this.handleSubmit = (e) => {
            e.preventDefault();
            console.log(this.props.queueForUpdate);
            console.log(this.props.queueForUpdateBoolean);
            csrfFetch('api/v1.0/statuses/new', {
                method: "POST",
                body: JSON.stringify({
                    queueForUpdate: this.props.queueForUpdate,
                    queueForUpdateBoolean: this.props.queueForUpdateBoolean,
                    comment: this.state.comment,
                    new_status: this.state.new_status
                })
            }).then((response) => {
                console.log(response);
                return response.json()
            }).then((json) => {
                this.setState({
                    comment: '',
                    new_status: this.state.new_status
                });
                console.log(this.state.new_status)
                for (var i = 0; i < this.props.queueForUpdateBoolean.length; i++) {
                    if (this.props.queueForUpdateBoolean[i]) {
                        this.props.updateStatus(this.props.queueForUpdate[i].toString(), this.state.new_status);
                    }
                }
            });

            this.handleClose();
            swal("Batch Status Update Success", '', "success");
            this.props.clearQueue();
        };
    }

    render() {
        return (
            <Modal
                trigger={<Button onClick={() => {
                    this.handleOpen()
                }} compact size='small' floated='right'>Update Multiple Status</Button>}
                open={this.state.modalOpen}
                onClose={this.state.handleClose}>
                <Modal.Header>
                    <Modal.Content>
                        <Modal.Description>
                            <Header>
                                <p>Current Suborders - {this.props.queueForUpdate.filter(i => i !== '')}</p>
                                <Form onSubmit={this.handleSubmit}>
                                    <Form.Select label='Change statuses to' fluid selection options={this.statuses}
                                                 onChange={(e, {value}) => {
                                                     this.setState({new_status: value})
                                                 }}
                                                 value={this.state.new_status}
                                    />
                                    <Form.Field id='form-textarea-control-opinion' control={TextArea}
                                                label='Leave an Additional Comment' placeholder='Comment'
                                                maxLength="200"
                                                onChange={(e, {value}) => {
                                                    this.setState({comment: value})
                                                }}
                                                value={this.state.comment}
                                    />
                                </Form>
                            </Header>
                        </Modal.Description>
                    </Modal.Content>
                </Modal.Header>
                <Modal.Actions>
                    <Button negative onClick={this.handleClose}>Cancel</Button>
                    <Button type='submit' positive onClick={this.handleSubmit} content="Confirm"/>
                </Modal.Actions>
            </Modal>
        )
    }
}

export default BatchStatusModal