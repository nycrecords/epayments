import React from 'react';
import {Grid, Container, Header, Divider} from 'semantic-ui-react';
import OrderForm from "./order_form";
import Order from "./order";


//Separates the page into three columns: The search form, divider, and orders list.
class App extends React.Component {
    render() {
        return (
            <Container>
                <Grid  columns={2}>
                    <Grid.Column width={4}>
                        <Header as="h1" textAlign="center">Epayments
                            <div className="sub header">Department of Records</div>
                        </Header>
                        <OrderForm/>
                    </Grid.Column>
                    <Grid.Column width={12}>
                        <Header as="h1" dividing textAlign="center">Orders</Header>
                        <Order/>
                    </Grid.Column>
                </Grid>
            </Container>
        )
    }
}


export default App
