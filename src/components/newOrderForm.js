import React, {} from 'react';
import {
    Route,
    Link
} from 'react-router-dom';

import {Button, Container, Divider, Grid, Header, Form, Loader, Dimmer, Icon, Segment} from 'semantic-ui-react';
import moment from 'moment';
import {csrfFetch, handleFetchErrors} from "../utils/fetch";
import SubOrderForm from "./suborderform";

class NewOrderForm extends React.Component {
    constructor() {
        super();
        this.state = {
            billingName: '',
            email: '',
            addressLine1: '',
            addressLine2: '',
            city: '',
            certified: [" "],
            state: '',
            zipCode: '',
            phone: '',
            instructions: '',
            orderType: [" "],
            deathPlace: [" "],
            cemetery: [" "],
            gender: [" "],
            fatherName: [" "],
            motherName: [" "],
            birthPlace: [" "],
            lastName: [" "],
            firstName: [" "],
            middleName: [" "],
            certificateNum: [" "],
            groomLastName: [" "],
            groomFirstName: [" "],
            brideLastName: [" "],
            brideFirstName: [" "],
            month: [" "],
            day: [" "],
            year: [" "],
            marriagePlace: [" "],
            letter: [false],
            block: [" "],
            lot: [" "],
            roll: [" "],
            borough: [" "],
            buildingNum: [" "],
            street: [" "],
            mail: [false],
            contactNum: [" "],

            imgId: [" "],
            imgTitle: [" "],
            comment: [" "],
            personalUseAgreement: [false],
            addDescription: [" "],
            collection: [" "],
            printSize: [" "],
            numCopies: [" "],
            status: [" "],

            showBirthCert: false,
            showBirthSearch: false,
            showDeathCert: false,
            showDeathSearch: false,
            showMarriageCert: false,
            showMarriageSearch: false,
            showTaxForm: false,
            showPhotoGalleryForm: false,
            showSubOrder: false,
            showPropertyForm: false,
            loading: false,
            subOrderList: [0]

        };

        this.handleChange = this.handleChange.bind(this);
        this.clearSelection = () => {
            this.setState({
                billingName: '',
                email: '',
                addressLine1: '',
                addressLine2: '',
                city: '',
                certified: [],
                state: '',
                zipCode: '',
                phone: '',
                instructions: '',
                orderType: [],
                deathPlace: [],
                cemetery: [],
                firstName: [],
                lastName: [],
                birthPlace: [],
                gender: [],
                fatherName: [],
                motherName: [],
                middleName: [],
                certificateNum: [],
                groomLastName: [],
                groomFirstName: [],
                brideLastName: [],
                brideFirstName: [],
                month: [],
                day: [],
                year: [],
                marriagePlace: [],
                letter: [],

                block: [],
                lot: [],
                roll: [],
                borough: [],
                buildingNum: [],
                street: [],
                mail: [],
                contactNum: [],
                imgId: [],
                imgTitle: [],
                comment: [],
                personalUseAgreement: [],
                addDescription: [],
                collection: [],
                printSize: [],
                numCopies: [],
                status: [],
            });
        };
        this.handleEmptyStates = () => {
            /*Add empty index to list whenever additional suborders are prompted
             to prevent null insert into DB if user left some fields unanswered
            */
            this.setState({
                certified: this.state.certified.concat([" "]),
                deathPlace: this.state.deathPlace.concat([" "]),
                cemetery: this.state.cemetery.concat([" "]),
                firstName: this.state.firstName.concat([" "]),
                lastName: this.state.lastName.concat([" "]),
                birthPlace: this.state.birthPlace.concat([" "]),
                gender: this.state.gender.concat([" "]),
                fatherName: this.state.fatherName.concat([" "]),
                motherName: this.state.motherName.concat([" "]),
                middleName: this.state.middleName.concat([" "]),
                certificateNum: this.state.certificateNum.concat([" "]),
                groomLastName: this.state.groomLastName.concat([" "]),
                groomFirstName: this.state.groomFirstName.concat([" "]),
                brideLastName: this.state.brideLastName.concat([" "]),
                brideFirstName: this.state.brideFirstName.concat([" "]),
                month: this.state.month.concat([" "]),
                day: this.state.day.concat([" "]),
                year: this.state.year.concat([" "]),
                marriagePlace: this.state.marriagePlace.concat([" "]),
                letter: this.state.letter.concat([false]),
                block: this.state.block.concat([" "]),
                lot: this.state.lot.concat([" "]),
                roll: this.state.roll.concat([" "]),
                borough: this.state.borough.concat([" "]),
                buildingNum: this.state.buildingNum.concat([" "]),
                street: this.state.street.concat([" "]),
                mail: this.state.mail.concat([false]),
                contactNum: this.state.contactNum.concat([" "]),
                imgId: this.state.imgId.concat([" "]),
                imgTitle: this.state.imgTitle.concat([" "]),
                comment: this.state.comment.concat([" "]),
                personalUseAgreement: this.state.personalUseAgreement.concat([false]),
                addDescription: this.state.addDescription.concat([" "]),
                collection: this.state.collection.concat([" "]),
                printSize: this.state.printSize.concat([" "]),
                numCopies: this.state.numCopies.concat([" "]),

            })

        };
        this.i = 0;
        this.index = 1;
        this.orderList = ['Tax Photo', 'Photo Gallery',
            'Property Card', 'Marriage Search',
            'Marriage Cert', 'Death Search',
            'Death Cert', 'Birth Search',
            'Birth Cert'];
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
    handleClick = () => {
        this.setState({subOrderList: this.state.subOrderList.concat([this.index])});
        this.index++;


    }

    handleSubmit = (e, value) => {
        e.preventDefault();
        // console.log("this is ordertype1: " + this.state.orderType);
        // console.log("num copies : " + this.state.numCopies);
        // console.log("gender:" + this.state.gender);
        // this.setState({loading: true});
        // if (this.state.orderType == '' && this.state.status == '') {
        //     alert("Please fill in Order Type and Status")
        //     this.setState({loading: false});
        //     return
        //
        // } else if (this.state.orderType == '') {
        //     alert("Please fill in Order Type")
        //     this.setState({loading: false});
        //     return
        // } else if (this.state.status == '') {
        //     alert("Please fill in Status")
        //     this.setState({loading: false});
        //     return
        // }
        // if (this.state.orderType != '') {
        //     if ((this.state.showBirthSearch == true || this.state.showBirthCert == true) && this.state.gender == '') {
        //         alert("Please fill in the Gender")
        //         this.setState({loading: false});
        //         return
        //
        //     }
        //     else if (this.state.showPropertyForm == true && this.state.borough == " ") {
        //         alert("Please fill in the Borough")
        //         this.setState({loading: false});
        //         return
        //     }
        //     else if (this.state.showPhotoGalleryForm == true && this.state.printSize == "") {
        //         alert("Please fill in the Printing Size")
        //         this.setState({loading: false});
        //         return
        //     }
        // }

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
                gender: this.state.gender,
                motherName: this.state.motherName,
                fatherName: this.state.fatherName,
                birthPlace: this.state.birthPlace,
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
                deathPlace: this.state.deathPlace,
                cemetery: this.state.cemetery,
                firstName: this.state.firstName,
                middleName: this.state.middleName,
                lastName: this.state.lastName,
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

    callBack = (dataFromChild, value, index, state) => {
        let newState = state.slice()
        newState[index] = value
        this.setState({
            [dataFromChild]: newState
        });
        console.log("State is : " + state);


    };

    render() {
        console.log('current list is ' + this.state.subOrderList);
        const SubOrders = this.state.subOrderList.map((suborderIndex) =>
            <Segment compact key={suborderIndex}>
                <h4>
                    Suborder: {suborderIndex + 1}
                </h4>
                <SubOrderForm
                    index={suborderIndex}
                    callBack={this.callBack}
                    state={this.state}
                />
            </Segment>
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
                                                required
                                                name="billingName"
                                                placeholder="Billing Name"
                                                maxLength="64"
                                                onChange={this.handleChange}
                                                value={this.state.billingName}
                                    />
                                    <Form.Input label="Email"
                                                required
                                                name="email"
                                                placeholder="Email"
                                                maxLength="64"
                                                onChange={this.handleChange}
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
                                    <Container>

                                        <Segment.Group compact>
                                            {SubOrders}

                                        </Segment.Group>
                                    </Container>
                                    <Button animated type="button" floated="left" onClick={() => {
                                        this.handleEmptyStates()
                                        this.handleClick()
                                    }}
                                    >
                                        <Button.Content visible>
                                            <Icon name='add'/>
                                        </Button.Content>
                                        <Button.Content hidden>
                                            Additional Order
                                        </Button.Content>
                                    </Button>
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