/**
 * Created by walwong on 8/13/18.
 */
import React from 'react';
import {Button, Header, Modal, Form, TextArea} from 'semantic-ui-react';
import 'semantic-ui-css/semantic.min.css';
import MarriageCert from '../order_type/marriage'
import MarriageSearch from '../order_type/marriage'


class OrderModal extends React.Component {
    constructor() {
        super();

        this.state = {
            modalOpen: false,

        };


        this.handleOpen = (e) => {
            e.preventDefault();

            switch(this.props.order_type) {
                case 'Marriage Cert':
                    this.marriageCert.get_info();

            }
            this.setState({
                modalOpen: true
            });
        };

        this.handleClose = (e) => this.setState({
            modalOpen: false,
        });
    }

    render() {
        const suborderInfo = (()=> {
            switch(this.props.order_type){
                case 'Marriage Cert':
                    return (
                         <MarriageCert
                             suborder_number={this.props.suborder_number}
                             ref={marriageCert => this.marriageCert = marriageCert}/>
                    );
                case'Marriage Search':
                    return(
                        <MarriageSearch
                            suborder_number={this.props.suborder_number}/>
                    );
            }
        });

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