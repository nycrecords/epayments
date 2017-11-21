/**
 * Created by sinsang on 5/23/17.
 */
import React from 'react';
import {Divider, Button} from 'semantic-ui-react';
import 'semantic-ui-css/semantic.min.css';
import StatusModal from './status_modal';
import History from './history';
import PhotoTaxModal from './photo_tax_modal'

class Order extends React.Component {
    render() {
        return (
            <div>
                <StatusModal current_status={this.props.current_status}
                             suborder_no={this.props.suborder_no}
                             updateStatus={this.props.updateStatus}
                />
                Order #: {this.props.order_no}
                <Button color="green" compact size='small' content={this.props.current_status} floated='right'/>
                <br/>
                Suborder #: {this.props.suborder_no} <br/>
                Order Type: {this.props.client_agency_name}
                { this.props.client_agency_name === 'Photo Tax' && <PhotoTaxModal suborder_no={this.props.suborder_no}/> }
                <br/>
                Billing Name: {this.props.billing_name} <br/>
                Date Submitted: {this.props.date_submitted} <br/>
                <History suborder_no={this.props.suborder_no} />
                <Divider/>
            </div>
        )
    }
}

export default Order