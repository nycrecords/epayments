import React from 'react';
import {Grid, Container, Header, Divider} from 'semantic-ui-react';
import OrderForm from "./order_form";

// class App extends React.Component {
//     render() {
//         return (
//             <Grid padded>
//                 <Grid.Row columns={2}>
//                     <Grid.Column>
//                         <Header as="h1">EPAYMENTS</Header>
//                             <OrderForm/>
//                     </Grid.Column>
//                         <Divider vertical/>
//                     <Grid.Column>
//                         <Container textAlign="center">
//                             Orders
//                         </Container>
//                     </Grid.Column>
//                 </Grid.Row>
//             </Grid>
//         );
//     }
// }

class App extends React.Component {
    render() {
        return (
            <Container padded>
                <Grid padded columns={3}>
                    <Grid.Column>
                        <Header as="h1" textAlign="center">Epayments
                            <div className="sub header">Department of Records</div>
                        </Header>
                        <OrderForm/>
                    </Grid.Column>
                    <Grid.Column>
                        <Divider vertical/>
                    </Grid.Column>
                    <Grid.Column>
                        <Header as="h1" dividing textAlign="center">Orders</Header>
                        <Grid.Row>One</Grid.Row>
                        <Grid.Row>Two</Grid.Row>
                        <Grid.Row>Three</Grid.Row>
                        <Grid.Row>Four</Grid.Row>
                        <Grid.Row>Five</Grid.Row>
                    </Grid.Column>
                </Grid>
            </Container>
        )
    }
}


export default App
