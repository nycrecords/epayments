import React from 'react';
import {Grid, Container, Header} from 'semantic-ui-react';
import OrderForm from "./order_form";


//Separates the page into three columns: The search form, divider, and orders list.
class App extends React.Component {
    render() {
        return (
            <Container>
                <Grid padded columns={3}>
                    <Grid.Column width={3}>
                        <Header as="h1" textAlign="center">Epayments
                            <div className="sub header">Department of Records</div>
                        </Header>
                        <OrderForm/>
                    </Grid.Column>
                    <Grid.Column width={1}/>
                    <Grid.Column width={11}>
                        <Header as="h1" dividing textAlign="center">Orders</Header>
                    </Grid.Column>
                </Grid>
            </Container>
        )
    }
}


export default App
