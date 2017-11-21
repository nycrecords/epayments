import React from 'react';
import {Button, Header, Modal, Form, TextArea} from 'semantic-ui-react';
import 'semantic-ui-css/semantic.min.css';

class StatusModal extends React.Component {
    constructor() {
        super();

        this.state = {
            modalOpen: false,
            comment: '',
            new_status: ''
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
                text: 'Done',
                value: 'Done',
            }

        ];

        this.handleSubmit = (e) => {
            e.preventDefault();
            fetch('api/v1.0/status/' + this.props.suborder_number, {
                method: "POST",
                body: JSON.stringify({
                    suborder_number: this.props.suborder_number,
                    comment: this.state.comment,
                    new_status: this.state.new_status
                })
            }).then((response) => {
                return response.json()
            }).then((json) => {
                json.status_code === 201 && this.props.updateStatus(this.props.suborder_number, this.state.new_status)
            });

            this.handleClose();
        };
    }

    render() {
        return (
            <Modal
                trigger={<Button onClick={this.handleOpen} compact size='small' floated='right'>Update Status</Button>}
                open={this.state.modalOpen}
                onClose={this.state.handleClose}>
                <Modal.Header>
                    <Modal.Content>
                        <Modal.Description>
                            <Header>
                                <p> Current Status - {this.props.current_status}</p>
                                <Form onSubmit={this.handleSubmit}>
                                    <Form.Select fluid selection options={this.statuses} placeholder={this.props.current_status}
                                                 onChange={(e, {value}) => {
                                                     this.setState({new_status: value})
                                                 }

                                                 }
                                                 value={this.state.new_status}
                                    />
                                    <Form.Field id='form-textarea-control-opinion' control={TextArea}
                                                label='Leave an Additional Comment' placeholder='Comment'
                                                onChange={(e, {value}) => {
                                                    this.setState({comment: value})
                                                }

                                                }
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

export default StatusModal