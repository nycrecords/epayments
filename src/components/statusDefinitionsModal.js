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
                        <strong>Received</strong> - When an order is imported<br/>
                        <strong>Microfilm</strong> - When an order needs to be printed from the Microfilm<br/>
                        <strong>Offsite</strong> - Has to be ordered from Offsite to be fulfilled<br/>
                        <strong>Processing</strong> - For photo orders only<br/>
                        <strong>Not Found</strong> - A Not Found Letter was sent to the customer<br/>
                        <strong>Undeliverable</strong> - When an order is returned as undeliverable by USPS / Email<br/>
                        <strong>Refund</strong> - The order has been sent to Administration for a refund<br/>
                        <strong>Done</strong> - The order has been completed. No more work is needed<br/>
                    </div>
                    <br/>
                    <Button type='button' negative onClick={this.handleClose} floated='right'>Close</Button>
                    <br/><br/>
                </Modal.Content>
            </Modal>
        )
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(StatusDefinitionsModal)
