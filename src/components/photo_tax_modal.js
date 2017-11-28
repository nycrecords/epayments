import React from 'react';
import {Button, Header, Modal, Form} from 'semantic-ui-react';
import 'semantic-ui-css/semantic.min.css';
import {csrfFetch} from "../utils/fetch"


class PhotoTaxModal extends React.Component {
    constructor() {
        super();

        this.state = {
            modalOpen: false,
            block_no: '',
            lot_no: '',
            roll_no: ''
        };

        this.handleOpen = (e) => {
            csrfFetch('api/v1.0/photo_tax/' + this.props.suborder_number).then((response) => (
                response.json()
            )).then((json) => {
                this.setState({
                    modalOpen: true,
                    block_no: json.block_no,
                    lot_no: json.lot_no,
                    roll_no: json.roll_no
                });
            });
        };

        this.handleClose = (e) => this.setState({
            modalOpen: false,
        });

        this.handleSubmit = (e) => {
            e.preventDefault();
            csrfFetch('api/v1.0/photo_tax/' + this.props.suborder_number, {
                method: "POST",
                body: JSON.stringify({
                    suborder_number: this.props.suborder_number,
                    block_no: this.state.block_no,
                    lot_no: this.state.lot_no,
                    roll_no: this.state.roll_no
                })
            }).then((response) => {
                return response.json()
            }).then((json) => {
                // this.props.updateStatus(this.props.suborder_number, this.state.new_status)
            });

            this.handleClose();
        };
    }

    render() {
        return (
            <Modal
                trigger={<Button onClick={this.handleOpen} compact size='small' floated='right'>Update Block/Lot/Roll</Button>}
                open={this.state.modalOpen}
                onClose={this.state.handleClose}>
                <Modal.Header>
                    <Modal.Content>
                        <Modal.Description>
                            <Header>
                                <p>Update the Block/Lot/Roll #</p>
                                <Form onSubmit={this.handleSubmit}>
                                    <Form.Input label="Block #" maxLength="9"
                                                onChange={(e, {value}) => {
                                                    this.setState({block_no: value})
                                                }}
                                                value={this.state.block_no}
                                    />
                                    <Form.Input label="Lot #" maxLength="9"
                                                onChange={(e, {value}) => {
                                                    this.setState({lot_no: value})
                                                }}
                                                value={this.state.lot_no}
                                    />
                                    {/* 1940s Only */}
                                    <Form.Input label="Roll #" maxLength="9"
                                                onChange={(e, {value}) => {
                                                    this.setState({roll_no: value})
                                                }}
                                                value={this.state.roll_no}
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

export default PhotoTaxModal