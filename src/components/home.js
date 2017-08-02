import React from 'react';
import {Grid, Container, Header, Button} from 'semantic-ui-react';
import OrderForm from "./order_form";
import Order from "./order";
// import "../data/orders.json";

class Home extends React.Component {
    state = {
        all_orders: []
    };

    componentWillMount() {
        fetch('api/v1.0/orders').then((response) => (
            response.json()
        )).then((json) => {
            this.setState({
                all_orders: json.all_orders
            });
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
            />

        )
        return (
            <Container>
                <Grid padded columns={3}>
                    <Grid.Column width={4}>
                        <Header as="h1" textAlign="center">Epayments
                            <Container className="sub header">Department of Records</Container>
                        </Header>
                        <OrderForm/>
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
