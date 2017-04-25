import React from 'react';
import {Grid, Container, Header, Divider} from 'semantic-ui-react';
import OrderForm from "./OrderForm";
// import './index.css';


class App extends React.Component {
    render() {
        return (
            <Grid divided="vertically">
                <Grid.Row columns={3}>
                    <Grid.Column>
                        <Container textAlign="center">
                            <Header as="h1">EPAYMENTS</Header>
                            <Header as="h2" className="tagline">Department of Records</Header>
                        </Container>
                        <Container >
                            <OrderForm/>
                        </Container>
                    </Grid.Column>
                    <Grid.Column>
                        <Divider vertical/>
                    </Grid.Column>
                    <Grid.Column>
                        <Container textAlign="center">
                            <h1>ORDERS SECTION</h1>
                        </Container>
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        );
    }
}


export default App
