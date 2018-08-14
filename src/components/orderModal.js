/**
 * Created by walwong on 8/13/18.
 */
import React from 'react';
import {Button, Header, Modal, Form, TextArea} from 'semantic-ui-react';
import 'semantic-ui-css/semantic.min.css';
import {csrfFetch} from "../utils/fetch"
import MarriageCert from 'order_type/marriage.js'


class OrderModal extends React.Component {
    constructor() {
        super();

        this.state = {
            modalOpen: false,
            order_type:'',
            suborder_number:this.props.suborder_number
        };


        this.handleOpen = (e) => {
            e.preventDefault;

            switch(order_type) {
                case 'Marriage Cert':
                    this.MarriageCert;

            }
        };

        this.handleClose = (e) => this.setState({
            modalOpen: false,
        });
    }

    render() {
        switch(this.state.order_type){

        }
        return (
            <Modal
                trigger={<Button onClick={this.handleOpen} compact size='small' floated='right'>More Info</Button>}
                open={this.state.modalOpen}
                onClose={this.state.handleClose}>

                {suborderInfo}

                <Modal.Actions>
                    <Button negative onClick={this.handleClose}>Cancel</Button>
                </Modal.Actions>
            </Modal>
        )
    }
}

export default OrderModal