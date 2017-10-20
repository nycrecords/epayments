/**
 * Created by sinsang on 5/23/17.
 */
import React from 'react';
import {Divider} from 'semantic-ui-react';
import 'semantic-ui-css/semantic.min.css';
import { Label, Dropdown, Menu} from 'semantic-ui-react';
import StatusModal from './status_modal';
import History from './history';

const options = [
  { key: 1, text: 'Choice 1', value: 1 },
  { key: 2, text: 'Choice 2', value: 2 },
  { key: 3, text: 'Choice 3', value: 3 },
]
class Order extends React.Component {
    constructor(){
        super();
    }

    handleHistoryRequest() {
        fetch('api/v1.0/history/' + this.props.suborder_no).then((response) => (
            response.json()
        )).then((json) => {
        });
        console.log(this.props.suborder_no)
    };

    render() {
        return (
            <div>
                <StatusModal current_status={this.props.current_status}
                             suborder_no={this.props.suborder_no}
                             updateStatus={this.props.updateStatus}
                />
                Order #: {this.props.order_no}
                {/*<Button compact size='mini' floated='right' color="green">Status</Button>*/}
                <br/>
                Suborder #: {this.props.suborder_no} <br/>
                Order Type: {this.props.client_agency_name}
                {/*<Button basic color="green" compact size='mini' content='History' icon='chevron down'*/}
                                    {/*labelPosition='right' floated='right'/><br/>*/}

                {/*<Menu compact size='mini' floated='right'>*/}
                  {/*<Dropdown text='History' color={'green'} onClick={this.handleHistoryRequest()} options={options} item/>*/}
                {/*</Menu>*/}

                <br/>
                Billing Name: {this.props.billing_name} <br/>
                Date Received: {this.props.date_received} <br/>

                Current Status: <Label color='green' >
                    {this.props.current_status}
                </Label>

                <br/>
                <History suborder_no={this.props.suborder_no}
                         handleHistoryRequest={this.props.handleHistoryRequest}
                />





                <Divider/>
                {/*<br/>*/}
            </div>
        )
    }
}

export default Order