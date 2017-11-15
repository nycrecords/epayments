/**
 * Created by sinsang on 5/23/17.
 */
import React from 'react';
import {Divider} from 'semantic-ui-react';
import 'semantic-ui-css/semantic.min.css';
import { Label, Dropdown, Button} from 'semantic-ui-react';
import StatusModal from './status_modal';
import History from './history';

const options = [
  { key: 1, text: 'Choice 1', value: 1 },
  { key: 2, text: 'Choice 2', value: 2 },
  { key: 3, text: 'Choice 3', value: 3 },
];
class Order extends React.Component {
    constructor(){
        super();
    }

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
                {/*<Menu compact size='mini' floated='right'>*/}
                  {/*<Dropdown text='History' color={'green'} onClick={this.handleHistoryRequest()} options={options} item/>*/}
                {/*</Menu>*/}
                <br/>
                Billing Name: {this.props.billing_name} <br/>
                Date Submitted: {this.props.date_submitted} <br/>
                <History suborder_no={this.props.suborder_no} />
                <Divider/>
                {/*<br/>*/}
            </div>
        )
    }
}

export default Order