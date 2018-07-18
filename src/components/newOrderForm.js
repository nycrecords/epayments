import React from 'react';
import {
  BrowserRouter as Router,
  Route,
  Link
} from 'react-router-dom';

import OrderForm from "./order_form";
import {Button, Container, Dimmer, Divider, Grid, Header, Form, Loader, Segment} from 'semantic-ui-react';
import moment from 'moment';
import orderTypeOptions  from "./order_form.js";
import statusOptions from "./order_form.js";

class NewOrderForm extends React.Component {
    constructor() {
        super();

        this.state = {
            billingName: '',
            address: '',
            orderType: '',
            collection: '',
            printSize: '',
            numCopies: '',
            status: 'All'


        };

        this.clearSelection = () => {
            this.setState({
                billingName: '',
                address: '',
                orderType: '',
                collection: '',
                printSize: '',
                numCopies: '',
                status: 'All'
            });
            this.yesterday = moment().subtract(1, 'days');
            this.today = moment();
        }
    }


    render() {


        // const newOrder = () => (
        //     <div>
        //         <div>
        //             <Grid padded columns={3}>
        //                 <Grid.Column width={4} id="grid-column-search">
        //
        //                     <Link to="/">
        //                         <Header as="h1" textAlign="center">ePayments
        //                             <Container className="sub header">Department of Records</Container>
        //                         </Header>
        //                     </Link>
        //                 </Grid.Column>
        //             </Grid>
        //         </div>
        //         <div>
        //             <Grid.Column width={1}/>
        //             <Grid.Column width={11} id="grid-column-order">
        //                 <Header as="h1" dividing textAlign="center">New Order</Header>
        //
        //
        //                 <div>
        //                     {/*<Container>*/}
        //                         {/*<form className="ui form">*/}
        //                             {/*<div className="field">*/}
        //                                 {/*<label>First Name</label>*/}
        //                                 {/*<input placeholder="First Name"/>*/}
        //                             {/*</div>*/}
        //                             {/*<div className="field">*/}
        //                                 {/*<label>Last Name</label>*/}
        //                                 {/*<input placeholder="Last Name"/>*/}
        //                             {/*</div>*/}
        //                             {/*<div className="field">*/}
        //                                 {/*<div className="ui checkbox">*/}
        //                                     {/*<input type="checkbox" className="hidden" readOnly="" tabIndex="0"/>*/}
        //                                     {/*<label>I agree to the Terms and Conditions</label>*/}
        //                                 {/*</div>*/}
        //                             {/*</div>*/}
        //                             {/*<button type="submit" className="ui button" role="button">Submit</button>*/}
        //                         {/*</form>*/}
        //                     {/*</Container>*/}
        //
        //
        //
        //                 </div>
        //                 <div>
        //                     <Divider clearing/>
        //                 </div>
        //
        //
        //             </Grid.Column>
        //
        //         </div>
        //
        //
        //     </div>
        // );


        return (
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
                            <Container>
                                <form className="ui form">
                                    <div className="field">
                                        <label>First Name</label>
                                        <input placeholder="First Name"/>
                                    </div>
                                    <div className="field">
                                        <label>Last Name</label>
                                        <input placeholder="Last Name"/>
                                    </div>
                                    <div className="field">
                                        <div className="ui checkbox">
                                            <input type="checkbox" className="hidden" readOnly="" tabIndex="0"/>
                                            <label>I agree to the Terms and Conditions</label>
                                        </div>
                                    </div>
                                    <button type="submit" className="ui button" role="button">Submit</button>
                                </form>
                            </Container>



                        </div>
                        <div>
                            <Divider clearing/>
                        </div>


                    </Grid.Column>

                </div>


            </div>

        )
    };
}



export default NewOrderForm;