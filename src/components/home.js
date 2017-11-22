import React from 'react';
import {Grid, Container, Header, Button, Segment, Divider, Modal} from 'semantic-ui-react';
import OrderForm from "./order_form";
import Order from "./order";
import LoginModal from "./login_modal"

class Home extends React.Component {
    constructor() {
        super();

        this.state = {
            all_orders: [],
            order_count: 0,
            suborder_count: 0,
            authenticated: false
        };

        this.addOrder = (order_count, suborder_count, orders) => {
            this.setState({
                all_orders: orders,
                order_count: order_count,
                suborder_count: suborder_count
            });
        };

        this.updateStatus = (suborder_number, new_status) => {
            let status_obj = this.state.all_orders.find(obj => {
                return obj.suborder_number === suborder_number;
            });
            let idx = this.state.all_orders.indexOf(status_obj);
            let status = {"index": idx, "object": status_obj};
            status.object.current_status = new_status;
            let _all_orders = this.state.all_orders.slice();
            _all_orders[status.index] = status.object;
            this.setState({all_orders: _all_orders});
        };

        this.printOrderSheet = () => {
            // e.preventDefault();
            // fetch('api/v1.0/print/orders', {
            //     method: "POST",
            //     body: JSON.stringify({
            //         order_number: this.state.ordernumber,
            //         suborder_number: this.state.subordernumber,
            //         order_type: this.state.order_type,
            //         billing_name: this.state.billing_name,
            //         date_submitted_start: formatDate(this.dateSubmittedStart),
            //         date_submitted_end: formatDate(this.dateSubmittedEnd)
            //     })
            // }).then((response) => {
            //     return response.json()
            // });
        };

        this.printBigLabels = () => {
            //    links to Big Label print
        };

        this.printSmallLabels = () => {
            //    links to Small Label print
        };

        this.logOut = () => {
            fetch('api/v1.0/logout', {
                method: "DELETE",
            }).then((response) => (
                response.json()
            )).then((json) => {
                alert("Logged Out")
            });

        };
    };

    componentWillMount() {
        fetch('api/v1.0/orders').then((response) => (
            response.json()
        )).then((json) => {
            this.addOrder(json.order_count, json.suborder_count, json.all_orders);
        })
    }
    ;


    render() {
        const orderRows = this.state.all_orders.map((order, index) =>
            <Order
                key={order.suborder_number}
                order_number={order.order_number}
                suborder_number={order.suborder_number}
                client_agency_name={order.client_agency_name}
                billing_name={order.billing_name}
                date_submitted={order.date_submitted.slice(0, -9)}
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
                            <LoginModal />
                        </Segment>
                        <Button content='Logout' onClick={this.logOut}/>
                        <OrderForm addOrder={this.addOrder}/>
                    </Grid.Column>
                    <Grid.Column width={1}/>
                    <Grid.Column width={11}>
                        <Header as="h1" dividing textAlign="center">Order</Header>
                        <div>
                            <Button.Group size='medium' floated='right'>
                                <Button labelPosition='left' icon='print'
                                        content='Order Sheet' onClick={this.printOrderSheet}/>
                                <Button content='Big Labels' onClick={this.printBigLabels}/>
                                <Button content='Small Labels' onClick={this.printSmallLabels}/>
                            </Button.Group>
                            <strong>Number of Items: {this.state.suborder_count}</strong>
                            <br/>
                            <strong>Number of Orders: {this.state.order_count}</strong>
                        </div>
                        <div>
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
