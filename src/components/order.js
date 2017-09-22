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
        fetch('api/v1.0/status/' + this.props.suborder_no).then((response) => (
            response.json()
        )).then((json) => {
            this.setState({status: json.status});
            console.log(json[status]);
        })
    };

    render() {
        return (
            <div>
                <StatusModal/>
                Order #: {this.props.order_no}
                <Button compact size='mini' floated='right' color="green">Status</Button>
                <br/>
                Suborder #: {this.props.suborder_no} <br/>
                Order Type: {this.props.client_agency_name} <Button basic color="green" compact size='mini' content='History' icon='chevron down'
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