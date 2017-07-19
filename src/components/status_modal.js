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
            text: 'open',
            value: 'test',
        },
        {
            text: 'testing again',
            value: 'testing again',
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
                                    <Dropdown placeholder="Status" selection options={this.statuses}/>
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