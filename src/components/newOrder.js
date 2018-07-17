import React from 'react';
import {
  BrowserRouter as Router,
  Route,
  Link
} from 'react-router-dom';

import OrderForm from "./order_form";
import {Button, Container, Dimmer, Divider, Grid, Header, Form, Loader, Segment} from 'semantic-ui-react';

const newOrder = () => (
    <div>
                <div>
                <Grid padded columns={3}>
                <Grid.Column width={4} id="grid-column-search">

                    <Link to="/">
                    <Header as="h1" textAlign="center">ePayments
                        <Container className="sub header">Department of Records</Container>
                    </Header>
                    </Link>
                </Grid.Column>
                </Grid>
                </div>
            <div>
                <Grid.Column width={1}/>
                        <Grid.Column width={11} id="grid-column-order">
                            <Header as="h1" dividing textAlign="center">New Order</Header>


                            <div>


                            </div>
                            <div>
                                <Divider clearing/>
                            </div>


                        </Grid.Column>

            </div>


    </div>
);

export default newOrder;