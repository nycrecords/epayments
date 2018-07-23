import React, {} from 'react';
import {
    Route,
    Link
} from 'react-router-dom';

import {Button, Container, Divider, Grid, Header, Form, Loader, Dimmer} from 'semantic-ui-react';
import moment from 'moment';
import {csrfFetch, handleFetchErrors} from "../utils/fetch"

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

class NewOrderForm extends React.Component {
    constructor() {
        super();

        this.state = {
            billingName: '',
            email:'',
            addressLine1:'None',
            addressLine2: 'None',
            city:'',
            state:'',
            zipCode:'',
            phone:'None',
            instructions:'None',
            orderType: '',
            collection: '',
            printSize: '',
            numCopies: '',
            status: 'All',
            loading: false

        };

        this.handleChange = this.handleChange.bind(this);

        this.clearSelection = () => {
            this.setState({
                billingName: '',
                email:'',
                addressLine1: '',
                addressLine2:'',
                city:'',
                state:'',
                zipCode:'',
                phone:'',
                instructions:'',
                orderType: '',
                collection: '',
                printSize: '',
                numCopies: '',
                status: 'All'
            });
        };

        this.photosValueList = ['photos', 'Tax Photo', 'Photo Gallery'];
        this.yesterday = moment().subtract(1, 'days');
        this.today = moment();
    };

    handleChange = (e) => {
        const target = e.target;
        const value = target.value;
        const name = target.name;
        this.setState({
            [name]: value
        });
    };

    handleSubmit = (e) => {
        e.preventDefault();
        this.setState({loading : true});
        csrfFetch('api/v1.0/orders/new', {
            method: "POST",
            body: JSON.stringify({
                billingName: this.state.billingName,
                email:this.state.email,
                addressLine1: this.state.addressLine1,
                address_two_2:this.state.addressLine2,
                city:this.state.city,
                state:this.state.state,
                zipCode:this.state.zipCode,
                phone:this.state.phone,
                instructions:this.state.instructions,
                orderType: this.state.orderType,
                collection: this.state.collection,
                printSize: this.state.printSize,
                numCopies: this.state.numCopies,
                status: this.state.status
            })
        })
                .then(handleFetchErrors)
                .then((json) => {
                    this.setState({loading : false});
                    window.open(json.url);

                }).catch((error) => {
                    console.error(error);
                    this.setState({loading : false});
                });

    };

    render() {
        // const OrderForm = () => (
        //
        //    
        //
        //
        // );

        return (
            <div>
                <Dimmer inverted active={this.state.loading}>
                    <Loader content='Loading'/>
                </Dimmer>
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
                                <Form onSubmit={this.handleSubmit}>
                                    <Form.Input label="Billing Name"
                                                name="billingName"
                                                placeholder="Billing Name"
                                                maxLength="64"
                                                width={8}
                                                onChange={this.handleChange}
                                                value={this.state.billingName}
                                    />
                                    <Form.Input label="Email"
                                                name="email"
                                                placeholder="Email"
                                                maxLength="64"
                                                width={8}
                                                onChange={this.handleChange}
                                                value={this.state.email}
                                    />
                                    <Form.Input label="Address line 1"
                                                name="addressLine1"
                                                placeholder="Address"
                                                maxLength="64"
                                                width={8}
                                                onChange={this.handleChange}
                                                value={this.state.addressLine1}
                                    />
                                    <Form.Input label="Address line 2"
                                                name="addressLine2"
                                                placeholder="Address"
                                                maxLength="64"
                                                width={8}
                                                onChange={this.handleChange}
                                                value={this.state.addressLine2}
                                    />
                                    <Form.Group>
                                        <Form.Input label="City"
                                                    name="city"
                                                    placeholder="City"
                                                    maxLength="64"
                                                    width={4}
                                                    onChange={this.handleChange}
                                                    value={this.state.city}
                                        />
                                        <Form.Input label="State"
                                                    name="state"
                                                    placeholder="State"
                                                    maxLength="64"
                                                    width={4}
                                                    onChange={this.handleChange}
                                                    value={this.state.state}
                                        />
                                        <Form.Input label="Zip Code"
                                                    name="zipCode"
                                                    placeholder="Zip Code"
                                                    maxLength="5"
                                                    width={4}
                                                    onChange={this.handleChange}
                                                    value={this.state.zipCode}
                                        />
                                    </Form.Group>
                                    <Form.Input label="Phone"
                                                name="phone"
                                                placeholder="Phone"
                                                maxLength="64"
                                                width={8}
                                                onChange={this.handleChange}
                                                value={this.state.phone}
                                    />
                                    <Form.Input label="Instructions"
                                                name="instructions"
                                                placeholder="Instructions"
                                                maxLength="64"
                                                width={8}
                                                onChange={this.handleChange}
                                                value={this.state.instructions}
                                    />
                                    <Form.Select label="Order Type"
                                                 name="orderType"
                                                 placeholder="Order Type"
                                                 options={orderTypeOptions}
                                                 width={8}
                                                 onChange={(e, {value}) => {
                                                     this.setState({orderType: value});
                                                 }}
                                                 value={this.state.orderType}
                                    />
                                    <Form.Input label="Collection"
                                                name="collection"
                                                placeholder="Collection"
                                                maxLength="64"
                                                width={8}
                                                onChange={this.handleChange}
                                                value={this.state.collection}
                                    />
                                    <Form.Group inline>
                                        <label>Printing Size</label>
                                        <Form.Radio
                                            name={"printSize"}
                                            label='Small'
                                            onChange={(e, {}) =>{
                                                this.setState({printSize: "Small"})
                                            }}
                                            value={this.state.printSize}
                                        />
                                        <Form.Radio
                                            name={"printSize"}
                                            label='Medium'
                                            onChange={(e, {}) =>{
                                                this.setState({printSize: "Medium"})
                                            }}
                                            value={this.state.printSize}
                                        />
                                        <Form.Radio
                                            name={"printSize"}
                                            label='Large'
                                            onChange={(e, {}) =>{
                                                this.setState({printSize: "Large"})
                                            }}
                                            value={this.state.printSize}
                                        />
                                    </Form.Group>
                                    <Form.Input label="Number of Copies"
                                                name="numCopies"
                                                placeholder="Number of Copies"
                                                maxLength="2"
                                                width={8}
                                                onChange={(e, {value}) => {
                                                    if (/^[0-9]+$/.test(value.slice(-1)) || value === '') {
                                                        this.handleChange(e)
                                                    }
                                                }}
                                                value={this.state.numCopies}
                                    />
                                    <Form.Select label="Status"
                                                 name="status"
                                                 placeholder="Status"
                                                 options={statusOptions}
                                                 width={8}
                                                 onChange={(e, {value}) => {
                                                     this.setState({status: value})
                                                 }}
                                                 value={this.state.status}
                                    />
                                    <Button type='submit' positive floated="left" content="Place Order"/>
                                    <Button type="reset" onClick={this.clearSelection} content="Clear"/>
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
};


export default NewOrderForm;