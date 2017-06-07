import React from 'react';
import {Grid, Container, Header, Button} from 'semantic-ui-react';
import OrderForm from "./order_form";
import Order from "./order"


//Separates the page into three columns: The search form, divider, and orders list.
var order = [];

for (var i = 0; i < 40; i++) {
    order.push(<Order/>);
}

class Home extends React.Component {
    render() {
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
                        {order}
                    </Grid.Column>
                </Grid>
                <Grid>
                    <Container id="load-more" width={5}>
                        <Button compact floated="right">Load More</Button>
                    </Container>
                </Grid>
            </Container>

        )
    }
}


export default Home
