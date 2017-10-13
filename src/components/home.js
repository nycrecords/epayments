import React from 'react';
import {Grid, Container, Header, Button} from 'semantic-ui-react';
import OrderForm from "./order_form";
import Order from "./order";
import StatusModal from "./status_modal";

// import "../data/orders.json";

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

        // this.update_status = (new_status) => {
        //     this.setState({
        //         current_status: new_status
        //     })
        // }
    };

    componentWillMount() {
        fetch('api/v1.0/orders').then((response) => (
            response.json()
        )).then((json) => {
            this.addOrder(json.all_orders)
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
                date_received={order.date_received}
                current_status={order.current_status}
            />

        );

        return (
            <Container>
                <Grid padded columns={3}>
                    <Grid.Column width={4}>
                        <Header as="h1" textAlign="center">Epayments
                            <Container className="sub header">Department of Records</Container>
                        </Header>
                        <OrderForm addOrder={this.addOrder}/>
                    </Grid.Column>
                    <Grid.Column width={1}/>
                    <Grid.Column width={11}>
                        <Header as="h1" dividing textAlign="center">Orders</Header>
                        {orderRows}
                    </Grid.Column>
                </Grid>
                <Grid>
                    <Container id="load-more" width={2}>
                        <Button compact floated="right">Load More</Button>
                    </Container>
                </Grid>
            </Container>

        )
    }
}


export default Home
