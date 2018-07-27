import React, {} from 'react';
import {
    Route,
    Link
} from 'react-router-dom';

import {Button, Container, Divider, Grid, Header, Form, Loader, Dimmer} from 'semantic-ui-react';
import moment from 'moment';
import {csrfFetch, handleFetchErrors} from "../utils/fetch"

const boroughOptions = [
    {key: 'bronx', text: 'Bronx', value: 'Bronx'},
    {key: 'brooklyn', text: 'Brooklyn', value: 'Brooklyn'},
    {key: 'manhattan', text: 'Manhattan', value: 'Manhattan'},
    {key: 'queens', text: 'Queens', value: 'Queens'},
    {key: 'statenisland', text: 'Staten Island', value: 'Staten Island'},
]

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
            certified: '',
            state: '',
            zipCode: '',
            phone: '',
            instructions: '',
            orderType: '',

            certificateNum: '',
            groomLastName: '',
            groomFirstName: '',
            brideLastName: '',
            brideFirstName: '',
            month: '',
            day: '',
            year: '',
            marriagePlace: '',
            letter: '',


            block: '',
            lot: '',
            row: '',
            borough: '',
            buildingNum: '',
            street: '',
            mail: '',
            contactNum: '',

            imgId: '',
            imgTitle: '',
            comment: '',
            personalUseAgreement: '',
            addDescription: '',
            collection: '',
            printSize: '',
            numCopies: '',
            status: '',

            showMarriageCert: false,
            showMarriageSearch: false,
            showTaxForm: false,
            showPhotoGalleryForm: false,
            showPropertyForm: false,
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
                certified: '',
                state: '',
                zipCode: '',
                phone: '',
                instructions: '',
                orderType: '',

                certificateNum: '',
                groomLastName: '',
                groomFirstName: '',
                brideLastName: '',
                brideFirstName: '',
                month: '',
                day: '',
                year: '',
                marriagePlace: '',
                letter: '',

                block: '',
                lot: '',
                roll: '',
                borough: '',
                buildingNum: '',
                street: '',
                mail: '',
                contactNum: '',
                imgId: '',
                imgTitle: '',
                comment: '',
                personalUseAgreement: '',
                addDescription: '',
                collection: '',
                printSize: '',
                numCopies: '',
                status: ''
            });
        };

        this.orderList = ['Tax Photo', 'Photo Gallery', 'Property Card', 'Marriage Search', 'Marriage Cert'];
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
                certified: this.state.certified,
                state: this.state.state,
                zipCode: this.state.zipCode,
                phone: this.state.phone,
                instructions: this.state.instructions,
                orderType: this.state.orderType,

                certificateNum: this.state.certificateNum,
                groomLastName: this.state.groomFirstName,
                groomFirstName: this.state.groomFirstName,
                brideLastName: this.state.brideLastName,
                brideFirstName: this.state.brideFirstName,
                month: this.state.month,
                day: this.state.day,
                year: this.state.year,
                marriagePlace: this.state.marriagePlace,
                letter: this.state.letter,

                block: this.state.block,
                lot: this.state.lot,
                roll: this.state.roll,
                borough: this.state.borough,
                buildingNum: this.state.buildingNum,
                street: this.state.street,
                mail: this.state.mail,
                contactNum: this.state.contactNum,
                imgId: this.state.imgId,
                imgTitle: this.state.imgTitle,
                comment: this.state.comment,
                personalUseAgreement: this.state.personalUseAgreement,
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
            <Grid>
                <Grid.Row>
                    <Grid.Column>
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
                                    onChange={this.handleChange}
                                    value={this.state.block}
                        />
                        <Form.Input label="Lot"
                                    name="lot"
                                    placeholder="Lot"
                                    onChange={this.handleChange}
                                    value={this.state.lot}
                        />
                        <Form.Input label="Roll"
                                    name="roll"
                                    placeholder="Roll#"
                                    onChange={this.handleChange}
                                    value={this.state.roll}
                        />
                        <Form.Group inline>
                            <label>Printing Size</label>

                            <Form.Radio
                                name={"printSize"}
                                label='8" x 10" Print'
                                checked={this.state.printSize === '"8 x 10" Print'}
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
                        <Form.Select label="Borough"
                                     name="borough"
                                     options={boroughOptions}
                                     placeholder="Borough"
                                     onChange={this.handleChange}
                                     value={this.state.value}
                        />
                        <Form.Input label="Building Number"
                                    name="buildingNum"
                                    placeholder="Building Number"
                                    onChange={this.handleChange}
                                    value={this.state.buildingNum}
                        />
                        <Form.Input label="Street"
                                    name="street"
                                    placeholder="Street"
                                    onChange={this.handleChange}
                                    value={this.state.street}
                        />
                        <Form.Input label="Mail"
                                    name="mail"
                                    placeholder="Mail"
                                    onChange={this.handleChange}
                                    value={this.state.mail}
                        />
                        <Form.Input label="description"
                                    name="addDescription"
                                    placeholder="Description"
                                    onChange={this.handleChange}
                                    value={this.state.addDescription}
                        />
                        <Form.Input label="Contact Number"
                                    name="contactNum"
                                    placeholder="Contact Number"
                                    onChange={this.handleChange}
                                    value={this.state.contactNum}
                        />
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        );
        const PropertyCardForm = () => (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Input label="Block"
                                    name="block"
                                    placeholder="Block"
                                    onChange={this.handleChange}
                                    value={this.state.block}
                        />
                        <Form.Input label="Lot"
                                    name="lot"
                                    placeholder="Lot"
                                    onChange={this.handleChange}
                                    value={this.state.lot}
                        />
                        <Form.Select label="Borough"
                                     name="borough"
                                     options={boroughOptions}
                                     placeholder="Borough"
                                     onChange={this.handleChange}
                                     value={this.state.value}
                        />
                        <Form.Input label="Building Number"
                                    name="buildingNum"
                                    placeholder="Building Number"
                                    onChange={this.handleChange}
                                    value={this.state.buildingNum}
                        />
                        <Form.Input label="Street"
                                    name="street"
                                    placeholder="Street"
                                    onChange={this.handleChange}
                                    value={this.state.street}
                        />
                        <Form.Input label="Mail"
                                    name="mail"
                                    placeholder="Mail"
                                    onChange={this.handleChange}
                                    value={this.state.mail}
                        />
                        <Form.Input label="description"
                                    name="addDescription"
                                    placeholder="Description"
                                    onChange={this.handleChange}
                                    value={this.state.addDescription}
                        />
                        <Form.Input label="Contact Number"
                                    name="contactNum"
                                    placeholder="Contact Number"
                                    onChange={this.handleChange}
                                    value={this.state.contactNum}
                        />
                        <Form.Input label="Certified"
                                    name="certified"
                                    placeholder="Certified"
                                    onChange={this.handleChange}
                                    value={this.state.certified}
                        />

                    </Grid.Column>
                </Grid.Row>
            </Grid>

        )
        const MarriageSearchForm = () => (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Group>
                            <Form.Input label="Groom First Name"
                                        name="groomFirstName"
                                        placeholder="Groom First Name"
                                        onChange={this.handleChange}
                                        value={this.state.groomFirstName}
                            />
                            <Form.Input label="Groom Last Name"
                                        name="groomLastName"
                                        placeholder="Groom Last Name"
                                        onChange={this.handleChange}
                                        value={this.state.groomLastName}
                            />
                        </Form.Group>
                        <Form.Group>
                            <Form.Input label="Bride First Name"
                                        name="brideFirstName"
                                        placeholder="Bride First Name"
                                        onChange={this.handleChange}
                                        value={this.state.brideFirstName}
                            />
                            <Form.Input label="Bride Last Name"
                                        name="BrideLastName"
                                        placeholder="Bride Last Name"
                                        onChange={this.handleChange}
                                        value={this.state.brideLastName}
                            />
                        </Form.Group>
                        <Form.Group>
                            <Form.Input label="Month"
                                        name="month"
                                        placeholder="Month"
                                        onChange={this.handleChange}
                                        value={this.state.month}
                            />
                            <Form.Input label="Day"
                                        name="day"
                                        maxLength={2}
                                        placeholder="Day"
                                        onChange={this.handleChange}
                                        value={this.state.day}
                            />
                            <Form.Input label="Year"
                                        name="year"
                                        maxLength={4}
                                        placeholder="Year"
                                        onChange={this.handleChange}
                                        value={this.state.year}
                            />
                        </Form.Group>

                        <Form.Select label="Borough"
                                     name="borough"
                                     options={boroughOptions}
                                     placeholder="Borough"
                                     onChange={this.handleChange}
                                     value={this.state.value}
                        />
                        <Form.Input label="Marriage Place"
                                    name="marriagePlace"
                                    placeholder="Marriage Place"
                                    onChange={this.handleChange}
                                    value={this.state.marriagePlace}
                        />
                        <Form.Input label="Letter"
                                    name="letter"
                                    placeholder="Letter"
                                    onChange={this.handleChange}
                                    value={this.state.letter}
                        />
                        <Form.Input label="Comment"
                                    name="comment"
                                    placeholder="Comment"
                                    onChange={this.handleChange}
                                    value={this.state.comment}
                        />
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
        const MarriageCertForm = () => (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Input label="Certificate Number"
                                    name="certificateNum"
                                    placeholder="Certificiate Number"
                                    onChange={this.handleChange}
                                    value={this.state.certificateNum}
                        />
                        {MarriageSearchForm()}

                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
        const PhotoGalleryForm = () => (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Input label="Image Identifier"
                                    name="imgId"
                                    placeholder="Image Identifier"
                                    onChange={this.handleChange}
                                    value={this.state.imgId}
                        />

                        <Form.Input label="Title/Description of Image"
                                    name="imgTitle"
                                    placeholder="Title/Description of Image"
                                    onChange={this.handleChange}
                                    value={this.state.imgTitle}
                        />

                        <Form.Input label="Addition Description"
                                    name="addDescription"
                                    placeholder="Addition Description"
                                    onChange={this.handleChange}
                                    value={this.state.addDescription}
                        />
                        <Form.Input label="Mail"
                                    name="mail"
                                    placeholder="Mail"
                                    onChange={this.handleChange}
                                    value={this.state.mail}
                        />
                        <Form.Input label="Contact Number"
                                    name="contactNum"
                                    placeholder="Contact Number"
                                    onChange={this.handleChange}
                                    value={this.state.contactNum}
                        />
                        <Form.Input label="Comment"
                                    name="comment"
                                    placeholder="Comment"
                                    onChange={this.handleChange}
                                    value={this.state.comment}
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
                            />

                            <Form.Radio
                                name={"printSize"}
                                label='11" x 14" Print'
                                checked={this.state.printSize === '11" x 14" Print'}
                                onChange={(e, {}) => {
                                    this.setState({printSize: '11" x 14" Print'})
                                }}
                            />

                            <Form.Radio
                                name={"printSize"}
                                label='16" x 20" Print'
                                checked={this.state.printSize === '16" x 20" Print'}
                                onChange={(e, {}) => {
                                    this.setState({printSize: '16" x 20" Print'})
                                }}
                            />

                        </Form.Group>
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        );

        return (
            <div>
                <Dimmer inverted active={this.state.loading}>
                    <Loader content='Loading'/>
                </Dimmer>
                <div>
                    <Grid>
                        <Grid.Row centered>
                            <Grid.Column>
                                <Link to="/">
                                    <Header as="h1" textAlign="center">ePayments
                                        <Container className="sub header">Department of Records</Container>
                                    </Header>
                                </Link>
                            </Grid.Column>
                        </Grid.Row>

                        <Grid.Row centered>
                            <Grid.Column>
                                <Header as="h1" dividing textAlign="center">New Order</Header>
                            </Grid.Column>
                        </Grid.Row>

                        <Grid.Row centered>
                            <Grid.Column width={6}>
                                <Form onSubmit={this.handleSubmit}>
                                    <Form.Input label="Billing Name"
                                                name="billingName"
                                                placeholder="Billing Name"
                                                maxLength="64"
                                                onChange={this.handleChange}
                                                value={this.state.billingName}
                                    />
                                    <Form.Input label="Email"
                                                name="email"
                                                placeholder="Email"
                                                maxLength="64"
                                                onChange={this.handleChange}
                                                value={this.state.email}
                                    />
                                    <Form.Input label="Address line 1"
                                                name="addressLine1"
                                                placeholder="Address"
                                                maxLength="64"
                                                onChange={this.handleChange}
                                                value={this.state.addressLine1}
                                    />
                                    <Form.Input label="Address line 2"
                                                name="addressLine2"
                                                placeholder="Address"
                                                maxLength="64"
                                                onChange={this.handleChange}
                                                value={this.state.addressLine2}
                                    />
                                    <Form.Group>

                                        <Form.Input label="City"
                                                    name="city"
                                                    placeholder="City"
                                                    maxLength="64"
                                                    onChange={this.handleChange}
                                                    value={this.state.city}
                                        />
                                        <Form.Input label="State"
                                                    name="state"
                                                    placeholder="State"
                                                    maxLength="64"
                                                    onChange={this.handleChange}
                                                    value={this.state.state}
                                        />
                                        <Form.Input label="Zip Code"
                                                    name="zipCode"
                                                    placeholder="Zip Code"
                                                    maxLength="5"
                                                    onChange={this.handleChange}
                                                    value={this.state.zipCode}
                                        />
                                    </Form.Group>

                                    <Form.Input label="Phone"
                                                name="phone"
                                                placeholder="Phone"
                                                maxLength="64"
                                                onChange={this.handleChange}
                                                value={this.state.phone}
                                    />
                                    <Form.Input label="Instructions"
                                                name="instructions"
                                                placeholder="Instructions"
                                                maxLength="64"
                                                onChange={this.handleChange}
                                                value={this.state.instructions}
                                    />
                                    <Form.Select label="Order Type"
                                                 name="orderType"
                                                 placeholder="Order Type"
                                                 options={orderTypeOptions}
                                                 onChange={(e, {value}) => {
                                                     this.setState({orderType: value});
                                                     //toggles hidden forms for Tax Photo if selected
                                                     (this.orderList.indexOf(value) == 0) ?
                                                         this.setState({showTaxForm: true}) :
                                                         this.setState({showTaxForm: false});
                                                     //toggles hidden forms for Photo Gallery if selected
                                                     (this.orderList.indexOf(value) == 1) ?
                                                         this.setState({showPhotoGalleryForm: true}) :
                                                         this.setState({showPhotoGalleryForm: false});
                                                     (this.orderList.indexOf(value) == 2) ?
                                                         this.setState({showPropertyForm: true}) :
                                                         this.setState({showPropertyForm: false});
                                                     (this.orderList.indexOf(value) == 3) ?
                                                         this.setState({showMarriageSearch: true}) :
                                                         this.setState({showMarriageSearch: false});
                                                     (this.orderList.indexOf(value) == 4) ?
                                                         this.setState({showMarriageCert: true}) :
                                                         this.setState({showMarriageCert: false});


                                                 }}
                                                 value={this.state.value}
                                    />

                                    {this.state.showTaxForm && TaxPhotoForm()}
                                    {this.state.showPhotoGalleryForm && PhotoGalleryForm()}
                                    {this.state.showPropertyForm && PropertyCardForm()}
                                    {this.state.showMarriageSearch && MarriageSearchForm()}
                                    {this.state.showMarriageCert && MarriageCertForm()}


                                    <Form.Input label="Number of Copies"
                                                name="numCopies"
                                                placeholder="Number of Copies"
                                                maxLength="2"
                                                onChange={(e, {value}) => {
                                                    if (/^[0-9]+$/.test(value.slice(-1)) || value === '') {
                                                        this.handleChange(e)
                                                    }
                                                }}
                                                value={this.state.value}
                                    />

                                    <Form.Select label="Status"
                                                 name="status"
                                                 placeholder="Status"
                                                 options={statusOptions}
                                                 onChange={(e, {value}) => {
                                                     this.setState({status: value});

                                                 }}
                                                 value={this.state.value}
                                    />


                                    <Button type='submit' positive floated="left" content="Place Order"/>
                                    <Button type="reset" onClick={this.clearSelection} content="Clear"/>
                                </Form>
                            </Grid.Column>
                        </Grid.Row>
                        <div>
                            <Divider clearing/>
                        </div>
                    </Grid>
                </div>
            </div>
        )
    };
}


export default NewOrderForm;