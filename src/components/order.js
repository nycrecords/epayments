/**
 * Created by sinsang on 5/23/17.
 */
import React from 'react';
import {Button, Divider, Header, Dropdown, Modal} from 'semantic-ui-react';
import 'semantic-ui-css/semantic.min.css';

class Order extends React.Component {
    render() {
        return (
            <div>
                Order #: {this.props.order_no}
                {/* TODO: Put in a new component!!!!!
                           */}
                <Modal trigger={<Button compact size='mini' floated='right'>Update</Button>}>
                    <Modal.Header>
                        <Modal.Content>
                            Status
                            <Modal.Description>
                                <Header>Status Content</Header>
                                <p>And Smaller Status Content</p>
                            </Modal.Description>
                        </Modal.Content>
                    </Modal.Header>
                    <Modal.Actions>
                        <Button negative>Cancel</Button>
                        <Button positive>Confirm</Button>
                    </Modal.Actions>
                </Modal>
                <Button compact size='mini' floated='right'>Status</Button>
                <br/>
                Suborder #: {this.props.suborder_no} <br/>
                Order Type: {this.props.order_type} <Button basic color="green" compact size='mini' content='History' icon='chevron down'
                                    labelPosition='right' floated='right'/><br/>
                Billing Name: {this.props.billing_name} <br/>
                Date Received: {this.props.date_received} <br/>
                <Divider/>
                <br/>
            </div>
        )
    }
}

export default Order