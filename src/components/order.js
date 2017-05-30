/**
 * Created by sinsang on 5/23/17.
 */
import React from 'react';
import {Button, Divider} from 'semantic-ui-react';
import 'semantic-ui-css/semantic.min.css';

class Order extends React.Component {
    render() {
        return (
            <div>
                Order #: <Button compact size='mini' floated='right'>Status</Button> <br/>
                Suborder #: <br/>
                Order Type: <Button basic color="green" compact size='mini' content='History' icon='chevron down' labelPosition='right' floated='right'/><br/>
                Billing Name:<br/>
                Date Received:<br/>
                <Divider/>
                <br/>
            </div>
        )
    }
}

export default Order