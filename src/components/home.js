import React from 'react';
import {Grid, Container, Header, Divider} from 'semantic-ui-react';
import OrderForm from "./order_form";


//Separates the page into three columns: The search form, divider, and orders list.
class App extends React.Component {
    render() {
        return (
            <Container>
                <Grid padded columns={3}>
                    <Grid.Column>
                        <Header as="h1" textAlign="center">Epayments
                            <div className="sub header">Department of Records</div>
                        </Header>
                        <OrderForm/>
                    </Grid.Column>
                    <Grid.Column>
                        {/*The divider needs its own grid or else it appears to the left of both components */}
                        <Divider vertical/>
                    </Grid.Column>
                    <Grid.Column>
                        <Header as="h1" dividing textAlign="center">Orders</Header>
                    </Grid.Column>
                </Grid>
            </Container>
        )
    }
}


export default App
