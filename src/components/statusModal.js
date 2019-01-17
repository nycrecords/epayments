import React from 'react';
import {Button, Form, Header, Modal, TextArea} from 'semantic-ui-react';
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
                    <Modal.Content>
                        <Modal.Description>
                            <Header>
                                <p>Current Status - {this.state.status}</p>
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