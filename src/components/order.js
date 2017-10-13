/**
 * Created by sinsang on 5/23/17.
 */
import React from 'react';
import {Button, Divider} from 'semantic-ui-react';
import 'semantic-ui-css/semantic.min.css';
import StatusModal from './status_modal';

class Order extends React.Component {
    constructor(){
        super();

        this.state = {
            status: []
        };

    }

    componentWillMount() {
        // fetch('api/v1.0/status/' + this.props.suborder_no).then((response) => (
        //     response.json()
        // )).then((json) => {
        //     this.setState({status: json.status});
        //     console.log(this.state.status)
        // })
    };

    render() {
        return (
            <div>
                <StatusModal current_status={this.props.current_status}
                             suborder_no={this.props.suborder_no}
                />
                Order #: {this.props.order_no}
                <Button compact size='mini' floated='right' color="green">Status</Button>
                <br/>
                Suborder #: {this.props.suborder_no} <br/>
                Order Type: {this.props.client_agency_name} <Button basic color="green" compact size='mini' content='History' icon='chevron down'
                                    labelPosition='right' floated='right'/><br/>
                Billing Name: {this.props.billing_name} <br/>
                Date Received: {this.props.date_received} <br/>
                Current Status: {this.props.current_status} <br/>

                <Divider/>
                <br/>
            </div>
        )
    }
}

export default Order