import React from 'react'
import {Button, Modal} from 'semantic-ui-react'
import {connect} from 'react-redux'
import {mapDispatchToProps, mapStateToProps} from "../utils/reduxMappers";


class StatusDefinitionsModal extends React.Component {

    constructor() {
        super();

        this.state = {
            modalOpen: false
        };

        this.handleOpen = (e) => this.setState({
            modalOpen: true,
        });

        this.handleClose = (e) => this.setState({
            modalOpen: false,
        });

    }

    render() {
        return (
            <Modal trigger={<Button onClick={this.handleOpen}>Status Definitions</Button>}
                   open={this.state.modalOpen}
                   onClose={this.state.handleClose}>
                <Modal.Header>Status Definitions</Modal.Header>
                <Modal.Content>
                    <div>
                        Received - When an order is imported<br/>
                        Microfilm - When an order needs to be printed from the Microfilm<br/>
                        Offsite - has been to be ordered to be fulfilled<br/>
                        Processing- For photo orders only<br/>
                        Not Found - A Not Found Letter was sent to the customer<br/>
                        Undeliverable - When an order is returned as undeliverable by USPS / Email<br/>
                        Refund - The order has been sent to Administration for a refund<br/>
                        Done - The order has been completed. No more work is needed<br/>
                    </div>
                    <Button type='button' negative onClick={this.handleClose} floated='right'>Close</Button>
                    <br/>
                </Modal.Content>
            </Modal>
        )
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(StatusDefinitionsModal)
