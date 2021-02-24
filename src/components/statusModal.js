import React from 'react';
import {Button, Form, Modal, TextArea} from 'semantic-ui-react';
import 'semantic-ui-css/semantic.min.css';
import {csrfFetch, handleFetchErrors} from "../utils/fetch"
import {statusOptions} from '../constants/constants'


class StatusModal extends React.Component {
    constructor() {
        super();

        this.state = {
            modalOpen: false,
            comment: '',
            status: ''
        };

        this.handleOpen = (e) => this.setState({
            modalOpen: true,
        });

        this.handleClose = (e) => this.setState({
            modalOpen: false,
        });

        this.handleSubmit = (e) => {
            e.preventDefault();
            csrfFetch('api/v1/status/' + this.props.suborder_number, {
                method: "PATCH",
                body: JSON.stringify({
                    suborder_number: this.props.suborder_number,
                    comment: this.state.comment,
                    status: this.state.status
                })
            })
                .then(handleFetchErrors)
                .then(() => {
                    this.props.updateStatus(this.props.suborder_number, this.state.status);
                    this.setState({comment: '', status: this.state.status});
                })
                .catch((error) => {
                    console.error(error);
                });
            this.handleClose();
        };
    }

    componentDidMount() {
        this.setState({status: this.props.current_status});
    }

    render() {
        return (
            <Modal
                trigger={<Button onClick={this.handleOpen} compact size='small' floated='right'>Update Status</Button>}
                open={this.state.modalOpen}
                onClose={this.state.handleClose}>
                <Modal.Header>
                    <p>Current Status - {this.state.status}</p>
                </Modal.Header>
                    <Modal.Content>
                        <div>
                            <strong>Received</strong> - When an order is imported<br/>
                            <strong>Microfilm</strong> - When an order needs to be printed from the Microfilm<br/>
                            <strong>Offsite</strong> - Has to be ordered from Offsite to be fulfilled<br/>
                            <strong>Processing</strong> - For photo orders only<br/>
                            <strong>Not Found</strong> - A Not Found Letter was sent to the customer<br/>
                            <strong>Undeliverable</strong> - When an order is returned as undeliverable by USPS /
                            Email<br/>
                            <strong>Refund</strong> - The order has been sent to Administration for a refund<br/>
                            <strong>Done</strong> - The order has been completed. No more work is needed<br/>
                        </div>
                        <br/>
                        <Modal.Description>
                                <Form onSubmit={this.handleSubmit}>
                                    <Form.Select fluid selection options={statusOptions.slice(1)}
                                                 onChange={(e, {value}) => {
                                                     this.setState({status: value})
                                                 }}
                                                 value={this.state.status}
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

                        </Modal.Description>
                    </Modal.Content>
                <Modal.Actions>
                    <Button negative onClick={this.handleClose}>Cancel</Button>
                    <Button type='submit' positive onClick={this.handleSubmit} content="Confirm"/>
                </Modal.Actions>
            </Modal>
        )
    }
}

export default StatusModal