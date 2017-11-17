import React from 'react';
import {Grid, Container, Header, Button, Segment, Divider} from 'semantic-ui-react';
import OrderForm from "./order_form";
import Order from "./order";

class Home extends React.Component {
    constructor() {
        super();

        this.state = {
            all_orders: []
        };

        this.addOrder = (orders) => {
            this.setState({
                all_orders: orders
            });
        };

        this.updateStatus = (suborder_no, new_status) => {
            let status_obj = this.state.all_orders.find(obj => {return obj.suborder_no === suborder_no; });
            let idx = this.state.all_orders.indexOf(status_obj);
            let status ={"index": idx, "object": status_obj};
            status.object.current_status = new_status;
            let _all_orders = this.state.all_orders.slice();
            _all_orders[status.index] = status.object;
            this.setState({all_orders: _all_orders});
        };
    };

    componentWillMount() {
        fetch('api/v1.0/orders').then((response) => (
            response.json()
        )).then((json) => {
            this.addOrder(json.all_orders);
        })
    };


    render() {
        const orderRows = this.state.all_orders.map((order, index) =>
            <Order
                key={order.suborder_no}
                order_no={order.order_no}
                suborder_no={order.suborder_no}
                client_agency_name={order.client_agency_name}
                billing_name={order.billing_name}
                date_submitted={order.date_submitted.slice(0,-9)}
                current_status={order.current_status}
                updateStatus={this.updateStatus}
            />
        );

        return (
            <Container>
                <Grid padded columns={3}>
                    <Grid.Column width={4}>
                        <Header as="h1" textAlign="center">Epayments
                            <Container className="sub header">Department of Records</Container>
                        </Header>
                        <Segment padded>
                            <Button primary fluid>Login</Button>
                        </Segment>
                        <OrderForm addOrder={this.addOrder}/>
                    </Grid.Column>
                    <Grid.Column width={1}/>
                    <Grid.Column width={11}>
                        <Header as="h1" dividing textAlign="center">Orders</Header>
                        <div>
                            <Button.Group size = 'medium' floated='right'>
                                <Button icon='print' content='Label Sheet'/>
                                <Button icon='print' content='Big Labels'/>
                                <Button icon='print' content='Small Labels'/>
                            </Button.Group>
                        </div>
                        <div>
                            <br/>
                             <br/>

                            <Divider clearing/>
                        </div>
                        {orderRows}
                    </Grid.Column>
                </Grid>
            </Container>

        )
    }
}


export default Home
