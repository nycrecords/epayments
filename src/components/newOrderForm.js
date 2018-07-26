import React, {} from 'react';
import {
    Route,
    Link
} from 'react-router-dom';

import {Button, Container, Divider, Grid, Header, Form, Loader, Dimmer} from 'semantic-ui-react';
import moment from 'moment';
import {csrfFetch, handleFetchErrors} from "../utils/fetch"
import Order from "./order";
import update from 'react-addons-update';


const orderTypeOptions = [
    {key: 'birthsearch', text: 'Birth Search', value: 'Birth Search'},
    {key: 'marriagesearch', text: 'Marriage Search', value: 'Marriage Search'},
    {key: 'deathsearch', text: 'Death Search', value: 'Death Search'},
    {key: 'birthcert', text: 'Birth Certificate', value: 'Birth Cert'},
    {key: 'marriagecert', text: 'Marriage Certificate', value: 'Marriage Cert'},
    {key: 'deathcert', text: 'Death Certificate', value: 'Death Cert'},
    {key: 'propertycard', text: 'Property Card', value: 'Property Card'},
    {key: 'taxphoto', text: 'Tax Photo', value: 'Tax Photo'},
    {key: 'photogallery', text: 'Photo Gallery', value: 'Photo Gallery'},
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
            email: '',
            addressLine1: '',
            addressLine2: '',
            city: '',
            state: '',
            zipCode: '',
            phone: '',
            instructions: '',
            orderType: '',
            block: '',
            lot: '',
            row: '',
            imgId: '',
            imgTitle: '',
            addDescription: '',
            collection: '',
            printSize: '',
            numCopies: '',
            status: '',
            showTaxForm: false,
            showPhotoGalleryForm: false,
            loading: false

        };

        this.handleChange = this.handleChange.bind(this);

        this.clearSelection = () => {
            this.setState({
                billingName: '',
                email: '',
                addressLine1: '',
                addressLine2: '',
                city: '',
                state: '',
                zipCode: '',
                phone: '',
                instructions: '',
                orderType: [],
                block: '',
                lot: '',
                roll: '',
                imgId: '',
                imgTitle: '',
                addDescription: '',
                collection: '',
                printSize: '',
                numCopies: '',
                status: ''
            });
        };

        this.photosValueList = ['Tax Photo', 'Photo Gallery'];
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

    handleArrayChange = (e) => {
        const target = e.target;
        const value = target.value;
        const name = target.name;
        this.setState({
            [name]: [this.state.name, value]
        });
    };

    handleSubmit = (e, value) => {
        e.preventDefault();
        this.setState({loading: true});
        csrfFetch('api/v1.0/orders/new', {
            method: "POST",
            body: JSON.stringify({
                billingName: this.state.billingName,
                email: this.state.email,
                addressLine1: this.state.addressLine1,
                address_two_2: this.state.addressLine2,
                city: this.state.city,
                state: this.state.state,
                zipCode: this.state.zipCode,
                phone: this.state.phone,
                instructions: this.state.instructions,
                orderType: this.state.orderType,
                block: this.state.block,
                lot: this.state.lot,
                roll: this.state.roll,
                imgId: this.state.imgId,
                imgTitle: this.state.imgTitle,
                addDescription: this.state.addDescription,
                collection: this.state.collection,
                printSize: this.state.printSize,
                numCopies: this.state.numCopies,
                status: this.state.status

            })
        })
            .then(handleFetchErrors)
            .then((json) => {
                this.setState({loading: false});
                window.open(json.url);

            }).catch((error) => {
            console.error(error);
            this.setState({loading: false});
        });

    };

    render() {
        const TaxPhotoForm = () => (
            <Container>
                <Grid>
                    <Grid.Row centered>
                        <Grid.Column width={8}>
                            <Form.Group inline>
                                <label>Collection</label>
                                <Form.Radio
                                    name="collection"
                                    label='1940s'
                                    checked={this.state.collection === "1940s"}
                                    onChange={(e, {}) => {
                                        this.setState({collection: "1940s"})
                                    }}

                                />
                                <Form.Radio
                                    name="collection"
                                    label='1980s'
                                    checked={this.state.collection === "1980s"}
                                    onChange={(e, {}) => {
                                        this.setState({collection: "1980s"})
                                    }}
                                />
                                <Form.Radio
                                    name="collection"
                                    label='Both'
                                    checked={this.state.collection === "Both"}
                                    onChange={(e, {}) => {
                                        this.setState({collection: "Both"})
                                    }}
                                />
                            </Form.Group>

                            <Form.Input label="Block"
                                        name="block"
                                        placeholder="Block"
                                        width={8}
                                        onChange={this.handleChange}
                                        value={this.state.block}
                            />
                            <Form.Input label="Lot"
                                        name="lot"
                                        placeholder="Lot"
                                        width={8}
                                        onChange={this.handleChange}
                                        value={this.state.lot}
                            />
                            <Form.Input label="Roll"
                                        name="roll"
                                        placeholder="Roll#"
                                        width={8}
                                        onChange={this.handleChange}
                                        value={this.state.roll}
                            />
                            <Form.Group inline>
                                <label>Printing Size</label>

                                <Form.Radio
                                    name={"printSize"}
                                    label='8" x 10" Print'
                                    checked={this.state.printSize ==='"8 x 10" Print'}
                                    onChange={(e, {}) => {
                                        this.setState({printSize: '"8 x 10" Print'})
                                    }}

                                />

                                <Form.Radio
                                    name={"printSize"}
                                    label='11" x 14" Print'
                                    checked={this.state.printSize === '"11 x 14" Print'}
                                    onChange={(e, {}) => {
                                        this.setState({printSize: '"11 x 14" Print'})
                                    }}
                                />
                            </Form.Group>
                        </Grid.Column>
                    </Grid.Row>
                </Grid>
            </Container>
        );
        const PhotoGalleryForm = () => (
            <Container>
                <Grid>
                    <Grid.Row centered>
                        <Grid.Column width={8}>
                            <Form.Input label="Image Identifier"
                                        name="imgId"
                                        placeholder="Image Identifier"
                                        width={8}
                                        onChange={this.handleChange}
                                        value={this.state.imgId}
                            />

                            <Form.Input label="Title/Description of Image"
                                        name="imgTitle"
                                        width={8}
                                        onChange={this.handleChange}
                                        value={this.state.imgTitle}
                            />

                            <Form.Input label="Addition Description"
                                        name="addDescription"
                                        width={8}
                                        onChange={this.handleChange}
                                        value={this.state.addDescription}
                            />

                            <Form.Group inline>
                                <label>Printing Size</label>

                                <Form.Radio
                                    name={"printSize"}
                                    label='8" x 10" Print'
                                    checked={this.state.printSize === '8" x 10" Print'}
                                    onChange={(e, {}) => {
                                        this.setState({printSize: '8" x 10" Print'})
                                    }}

                                    // value={this.state.printSize}
                                />

                                <Form.Radio
                                    name={"printSize"}
                                    label='11" x 14" Print'
                                    checked={this.state.printSize === '11" x 14" Print'}
                                    onChange={(e, {}) => {
                                        this.setState({printSize: '11" x 14" Print'})
                                    }}
                                    // value={this.state.printSize}
                                />

                                <Form.Radio
                                    name={"printSize"}
                                    label='16" x 20" Print'
                                    checked={this.state.printSize === '16" x 20" Print'}
                                    onChange={(e, {}) => {
                                        this.setState({printSize: '16" x 20" Print'})
                                    }}
                                    // value={this.state.printSize}
                                />

                            </Form.Group>
                        </Grid.Column>
                    </Grid.Row>
                </Grid>
            </Container>
        );

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
                    <Grid padded columns={3}>
                        <Grid.Row centered>
                            <Grid.Column width={12} id="grid-column-order">
                                <Header as="h1" dividing>New Order</Header>
                                <div>
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
                                                         this.setState({orderType : value});
                                                         console.log(value);
                                                         //toggles hidden forms for Tax Photo if selected
                                                         (this.photosValueList.indexOf(value) == 0) ?
                                                             this.setState({showTaxForm: true}) :
                                                             this.setState({showTaxForm: false});
                                                         //toggles hidden forms for Photo Gallery if selected
                                                         (this.photosValueList.indexOf(value) == 1) ?
                                                             this.setState({showPhotoGalleryForm: true}) :
                                                             this.setState({showPhotoGalleryForm: false});
                                                     }}
                                                     value={this.state.value}
                                        />

                                        {this.state.showTaxForm && TaxPhotoForm()}
                                        {this.state.showPhotoGalleryForm && PhotoGalleryForm()}

                                        <Form.Input label="Number of Copies"
                                                    name="numCopies"
                                                    placeholder="Number of Copies"
                                                    maxLength="2"
                                                    width={8}
                                                    onChange={(e, {value}) => {
                                                        if (/^[0-9]+$/.test(value.slice(-1)) || value === '') {
                                                            this.handleArrayChange(e)
                                                        }
                                                    }}
                                                    value={this.state.value}
                                        />

                                        <Form.Select label="Status"
                                                     name="status"
                                                     placeholder="Status"
                                                     options={statusOptions}
                                                     width={8}
                                                     onChange={(e, {value}) => {
                                                         this.setState({status: value});

                                                     }}
                                                     value={this.state.value}
                                        />


                                        <Button type='submit' positive floated="left" content="Place Order"/>
                                        <Button type="reset" onClick={this.clearSelection} content="Clear"/>
                                    </Form>
                                </div>
                                <div>
                                    <Divider clearing/>
                                </div>
                            </Grid.Column>
                        </Grid.Row>
                    </Grid>
                </div>
            </div>
        )
    };
};


export default NewOrderForm;