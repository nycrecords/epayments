/**
 * Created by sinsang on 5/23/17.
 */
import React from 'react';
import {Button, Divider, Checkbox} from 'semantic-ui-react';
import 'semantic-ui-css/semantic.min.css';
import StatusModal from './statusModal';
import History from './history';
import TaxPhotoModal from './taxPhotoModal';

class Order extends React.Component {
    render() {
        return (
            <div>
                <StatusModal current_status={this.props.current_status}
                             suborder_number={this.props.suborder_number}
                             updateStatus={this.props.updateStatus}
                />
                Order #: {this.props.order_number}
                <Button color="green" compact size='small' content={this.props.current_status} floated='right'/>
                <br/>
                Suborder #: {this.props.suborder_number}<br/>
                Order Type: {this.props.order_type}
                {this.props.order_type === "Tax Photo" && <TaxPhotoModal suborder_number={this.props.suborder_number}/>}
                <br/>
                Billing Name: {this.props.billing_name}
                <br/>
                Date Received: {this.props.date_received}
                <br/>
                <History suborder_number={this.props.suborder_number}/>
                <Checkbox label="Queue For Status Update"
                          checked={this.props.queueForUpdateBoolean === true}
                          onChange={() => {
                              this.props.addStatusQueue(this.props.order);

                          }}
                />
                <Divider/>
            </div>
        )
    }
}

export default Order