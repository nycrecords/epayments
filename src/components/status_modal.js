import React from 'react';
import {Button, Header, Modal, Form, TextArea, Dropdown} from 'semantic-ui-react';
import 'semantic-ui-css/semantic.min.css';

class StatusModal extends React.Component {
    state = {modalOpen: false};

    handleOpen = (e) => this.setState({
        modalOpen: true,
    });

    handleClose = (e) => this.setState({
        modalOpen: false,
    });
    statuses = [
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
            value: 'Not_found',
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


    render() {
        return (
            <Modal
                trigger={<Button onClick={this.handleOpen} compact size='mini' floated='right'>Update Status</Button>}
                open={this.state.modalOpen}
                onClose={this.state.handleClose}>
                <Modal.Header>
                    <Modal.Content>
                        <Modal.Description>
                            <Header>
                                <p> - Current Status - </p>
                                <Form>
                                    <Dropdown placeholder="Status" fluid selection options={this.statuses}/>
                                </Form>
                            </Header>
                            <Form>
                                <TextArea fluid placeholder='Tell us more'/>
                            </Form>
                        </Modal.Description>
                    </Modal.Content>
                </Modal.Header>
                <Modal.Actions>
                    <Button negative onClick={this.handleClose}>Cancel</Button>
                    <Button positive onClick={this.handleClose}>Confirm</Button>
                </Modal.Actions>
            </Modal>
        )
    }
}

export default StatusModal