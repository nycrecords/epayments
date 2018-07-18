import React, {Component} from 'react';
import {
    BrowserRouter as Router,
    Route,
    Link
} from 'react-router-dom';

import OrderForm from "./order_form";
import {Button, Container, Message, Divider, Grid, Header, Form, Loader, Segment} from 'semantic-ui-react';
import moment from 'moment';

const orderTypeOptions = [
    {key: 'all', text: 'All', value: 'all'},
    {key: 'vitalrecords', text: '--Vital Records--', value: 'vital_records'},
    {key: 'birthsearch', text: 'Birth Search', value: 'Birth Search'},
    {key: 'marriagesearch', text: 'Marriage Search', value: 'Marriage Search'},
    {key: 'deathsearch', text: 'Death Search', value: 'Death Search'},
    {key: 'birthcert', text: 'Birth Certificate', value: 'Birth Cert'},
    {key: 'marriagecert', text: 'Marriage Certificate', value: 'Marriage Cert'},
    {key: 'deathcert', text: 'Death Certificate', value: 'Death Cert'},
    {key: 'propertycard', text: 'Property Card', value: 'Property Card'},
    {key: 'photos', text: '--Photos--', value: 'photos'},
    {key: 'taxphoto', text: 'Tax Photo', value: 'Tax Photo'},
    {key: 'photogallery', text: 'Photo Gallery', value: 'Photo Gallery'},
    {key: 'other', text: '--Other--', value: 'other', disabled: true},
    {key: 'multipleincart', text: 'Multiple Items In Cart', value: 'multiple_items'},
    {key: 'vitalincart', text: 'Vital Records And Photos In Cart', value: 'vital_records_and_photos'}
];
const statusOptions = [
    {key: 'all', text: 'All', value: 'all'},
    {key: 'received', text: 'Received', value: 'Received'},
    {key: 'processing', text: 'Processing', value: 'Processing'},
    {key: 'found', text: 'Found', value: 'Found'},
    {key: 'printed', text: 'Printed', value: 'Printed'},
    {key: 'mailed/pickup', text: 'Mailed/Pickup', value: 'Mailed/Pickup'},
    {key: 'not_found', text: 'Not Found', value: 'Not_Found'},
    {key: 'letter_generated', text: 'Letter Generated', value: 'Letter_Generated'},
    {key: 'undeliverable', text: 'Undeliverable', value: 'Undeliverable'},
    {key: 'refunded', text: 'Refunded', value: 'Refunded'},
    {key: 'done', text: 'Done', value: 'Done'}
];
const copyOptions = [
    {key: '1', text: "1", value: "1"},
    {key: '2', text: "2", value: "2"},
    {key: '3', text: "3", value: "3"},
    {key: '4', text: "4", value: "4"},
    {key: '5', text: "5", value: "5"},
    {key: '6', text: "6", value: "6"},
    {key: '7', text: "7", value: "7"},
    {key: '8', text: "8", value: "8"},
    {key: '9', text: "9", value: "9"},
    {key: '10', text: "10", value: "10"}


]

class NewOrderForm extends React.Component {
    constructor() {
        super();

        this.state = {
            billingName: '',
            address: '',
            orderType: '',
            collection: '',
            printSize: '',
            numCopies: '0',
            status: 'All'


        };
        // this.handleChange = (e, { name, value }) => this.setState({ [name]: value })

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
        }
        this.photosValueList = ['photos', 'Tax Photo', 'Photo Gallery'];
        this.yesterday = moment().subtract(1, 'days');
        this.today = moment();

        this.submitFormData = (e, print) => {
            e.preventDefault();

            // switch(print){
            //     case 'orders':
            //     case 'large_labels':
            //     case 'small_labels':
            //         csrfFetch('api/v1.0/print/' + print, {
            //             method: "POST",
            //             body: JSON.stringify({
            //                 billingName: this.billingName,
            //                 address: this.address,
            //                 orderType: this.orderType,
            //                 collection: this.collection,
            //                 printSize: this.printSize,
            //                 numCopies: this.numCopies,
            //                 status: this.status
            //                 }
            //
            //             )
            //         }
            // }
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
                                <Form onSubmit={this.handleSubmit} success>
                                    {/*<Form.Group>*/}
                                    <Form.Input label="Billing Name" placeholder="Billing Name" maxLength="64" width={6}
                                                onChange={(e, {value}) => {
                                                    if (/^[a-zA-Z\s]*$/.test(value.slice(-1)) || value === '') {
                                                        this.setState({billing_name: value})
                                                    }
                                                }}
                                                value={this.state.billing_name}
                                    />
                                    <Form.Input label="Address" placeholder="Address" maxLength="64" width={8}
                                                onChange={(e, {value}) => {
                                                    if (/^[a-zA-Z\s]*$/.test(value.slice(-1)) || value === '') {
                                                        this.setState({Address: value})
                                                    }
                                                }}
                                                value={this.state.Address}
                                    />
                                    <Form.Select label="Order Type" placeholder="Order Type" options={orderTypeOptions}
                                                 width={6}
                                                 onChange={(e, {value}) => {
                                                     this.setState({orderType: value});

                                                     // Toggle visibility of "Generate CSV" button
                                                     (this.photosValueList.indexOf(value) > -1) ? this.props.toggleCSV(true) : this.props.toggleCSV(false);
                                                 }}
                                                 value={this.state.orderType}
                                    />
                                    <Form.Input label="Collection" placeholder="Collection" maxLength="64" width={6}
                                                onChange={(e, {value}) => {
                                                    if (/^[a-zA-Z\s]*$/.test(value.slice(-1)) || value === '') {
                                                        this.setState({collection: value})
                                                    }
                                                }}
                                                value={this.state.collection}
                                    />

                                    <Form.Group inline>
                                        <label>Printing Size</label>

                                        <Form.Radio
                                            name={"size"}
                                            label='Small'
                                            checked={(this.state.printSize =='Small')}
                                            onChange={(e, {value}) => {
                                                value = 'Small'
                                                this.setState({printSize: value})

                                            }}

                                        />
                                        <Form.Radio
                                            name={"size"}
                                            checked={(this.state.printSize =='Medium')}
                                            label='Medium'
                                            onChange={(e, {value}) => {
                                                value = 'Medium'
                                                this.setState({printSize: value})
                                            }}


                                        />
                                        <Form.Radio
                                            name={"size"}
                                            label='Large'
                                            checked={(this.state.printSize =='Large')}
                                            onChange={(e, {value}) => {
                                                value = 'Large'
                                                this.setState({printSize: value})
                                            }}
                                        />
                                    </Form.Group>

                                    <Form.Select Label="Number of Copies" placeholder="Number of Copies" options={copyOptions} width={6}
                                                 onChange={(e, {value}) => {
                                                     this.setState({numCopies: value})
                                                 }}
                                                 value={this.state.numCopies}
                                    />
                                    <Form.Select label="Status" placeholder="Status" options={statusOptions} width={6}
                                                 onChange={(e, {value}) => {
                                                     this.setState({status: value})
                                                 }}
                                                 value={this.state.status}
                                    />
                                    {/*<Message success header='Form Completed' content="You're all signed up for the newsletter" />*/}
                                    <Button type='submit' positive floated="left" content="Place Order" onChange/>
                                    <Button type="reset" onClick={this.clearSelection} content="Clear"/>
                                    {/*</Form.Group>*/}

                                </Form>
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