import React, {} from 'react';
import {
    Link
} from 'react-router-dom';
import {
    Button,
    Container,
    Divider,
    Grid,
    Header,
    Form,
    Loader,
    Dimmer,
    Icon,
    Segment,
} from 'semantic-ui-react';
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
            certified: [''],
            state: '',
            zipCode: '',
            phone: '',
            instructions: '',
            orderType: [''],
            deathPlace: [''],
            cemetery: [''],
            gender: [''],
            fatherName: [''],
            motherName: [''],
            birthPlace: [''],
            lastName: [''],
            firstName: [''],
            middleName: [''],
            certificateNum: [''],
            groomLastName: [''],
            groomFirstName: [''],
            brideLastName: [''],
            brideFirstName: [''],
            month: [''],
            day: [''],
            year: [''],
            marriagePlace: [''],
            letter: [false],
            block: [''],
            lot: [''],
            roll: [''],
            borough: [''],
            buildingNum: [''],
            street: [''],
            mail: [false],
            contactNum: [''],
            imgId: [''],
            imgTitle: [''],
            comment: [''],
            personalUseAgreement: [false],
            addDescription: [''],
            collection: [''],
            printSize: [''],
            numCopies: [''],
            status: [''],
            showBirthCert: [false],
            showBirthSearch: [false],
            showDeathCert: [false],
            showDeathSearch: [false],
            showMarriageCert: [false],
            showMarriageSearch: [false],
            showTaxForm: [false],
            showPhotoGalleryForm: [false],
            showSubOrder: [false],
            showPropertyForm: [false],
            loading: false,
            clearForm: false,
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
                certified: [''],
                state: '',
                zipCode: '',
                phone: '',
                instructions: '',
                orderType: [''],
                deathPlace: [''],
                cemetery: [''],
                firstName: [''],
                lastName: [''],
                birthPlace: [''],
                gender: [''],
                fatherName: [''],
                motherName: [''],
                middleName: [''],
                certificateNum: [''],
                groomLastName: [''],
                groomFirstName: [''],
                brideLastName: [''],
                brideFirstName: [''],
                month: [''],
                day: [''],
                year: [''],
                marriagePlace: [''],
                letter: [''],
                block: [''],
                lot: [''],
                roll: [''],
                borough: [''],
                buildingNum: [''],
                street: [''],
                mail: [false],
                contactNum: [''],
                imgId: [''],
                imgTitle: [''],
                comment: [''],
                personalUseAgreement: [false],
                addDescription: [''],
                collection: [''],
                printSize: [''],
                numCopies: [''],
                status: [''],
                showBirthCert: [false],
                showBirthSearch: [false],
                showDeathCert: [false],
                showDeathSearch: [false],
                showMarriageCert: [false],
                showMarriageSearch: [false],
                showTaxForm: [false],
                showPhotoGalleryForm: [false],
                showPropertyForm: [false],
            });
        };
        this.handleEmptyStates = () => {
            /*Add empty index to list whenever additional suborders are prompted
             to prevent null insert into DB if user left some fields unanswered
            */
            this.setState({
                    certified: this.state.certified.concat(['']),
                    deathPlace: this.state.deathPlace.concat(['']),
                    cemetery: this.state.cemetery.concat(['']),
                    firstName: this.state.firstName.concat(['']),
                    lastName: this.state.lastName.concat(['']),
                    birthPlace: this.state.birthPlace.concat(['']),
                    gender: this.state.gender.concat(['']),
                    fatherName: this.state.fatherName.concat(['']),
                    motherName: this.state.motherName.concat(['']),
                    middleName: this.state.middleName.concat(['']),
                    certificateNum: this.state.certificateNum.concat(['']),
                    groomLastName: this.state.groomLastName.concat(['']),
                    groomFirstName: this.state.groomFirstName.concat(['']),
                    brideLastName: this.state.brideLastName.concat(['']),
                    brideFirstName: this.state.brideFirstName.concat(['']),
                    month: this.state.month.concat(['']),
                    day: this.state.day.concat(['']),
                    year: this.state.year.concat(['']),
                    marriagePlace: this.state.marriagePlace.concat(['']),
                    letter: this.state.letter.concat([false]),
                    block: this.state.block.concat(['']),
                    lot: this.state.lot.concat(['']),
                    roll: this.state.roll.concat(['']),
                    borough: this.state.borough.concat(['']),
                    buildingNum: this.state.buildingNum.concat(['']),
                    street: this.state.street.concat(['']),
                    mail: this.state.mail.concat([false]),
                    contactNum: this.state.contactNum.concat(['']),
                    imgId: this.state.imgId.concat(['']),
                    imgTitle: this.state.imgTitle.concat(['']),
                    comment: this.state.comment.concat(['']),
                    personalUseAgreement: this.state.personalUseAgreement.concat([false]),
                    addDescription: this.state.addDescription.concat(['']),
                    collection: this.state.collection.concat(['']),
                    printSize: this.state.printSize.concat(['']),
                    numCopies: this.state.numCopies.concat(['']),
                    status: this.state.status.concat(['']),
                    orderType: this.state.orderType.concat(['']),
                    showMarriageSearch: this.state.showMarriageSearch.concat([false]),
                    showBirthSearch: this.state.showBirthSearch.concat([false]),
                    showBirthCert: this.state.showBirthCert.concat([false]),
                    showMarriageCert: this.state.showMarriageCert.concat([false]),
                    showDeathCert: this.state.showDeathCert.concat([false]),
                    showDeathSearch: this.state.showDeathSearch.concat([false]),
                    showTaxForm: this.state.showTaxForm.concat([false]),
                    showPhotoGalleryForm: this.state.showPhotoGalleryForm.concat([false]),
                    showPropertyForm: this.state.showPropertyForm.concat([false]),
        })
        };
        this.deleteSuborderValues = (index, state, name) => {
            let newState = state.slice();
            newState.splice(index, 1);
            for (var i = index; i < newState; i++) {
                newState[i] = newState[i - 1]
            }
            this.setState({[name]: newState})
        };
        this.index = 1;
        this.orderList = ['Tax Photo', 'Photo Gallery', 'Property Card', 'Marriage Search',
            'Marriage Cert', 'Death Search', 'Death Cert', 'Birth Search', 'Birth Cert'];
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
        this.setState({loading: true});
        for (var i = 0; i < this.state.subOrderList.length; i++) {
            if (this.state.orderType[i] === '' && this.state.status[i] === '') {
                alert("Please fill in Order Type and Status in Suborder: " + (i + 1))
                this.setState({loading: false});
                return

            } else if (this.state.orderType[i] === '') {
                alert("Please fill in Order Type in Suborder: " + (i + 1))
                this.setState({loading: false});
                return
            } else if (this.state.status[i] === '') {
                alert("Please fill in Status in Suborder: " + (i + 1))
                this.setState({loading: false});
                return
            }

            if (this.state.orderType[i] !== '') {
                if ((this.state.showBirthSearch[i] === true || this.state.showBirthCert === true[i]) && this.state.gender[i] === '') {
                    alert("Please fill in the Gender in Suborder: " + (i + 1))
                    this.setState({loading: false});
                    return
                }
                else if (this.state.showPropertyForm[i] === true && this.state.borough[i] === '') {
                    alert("Please fill in the Borough in Suborder:" + (i + 1))
                    this.setState({loading: false});
                    return
                }
                else if ((this.state.showPhotoGalleryForm[i] === true || this.state.showTaxForm[i] === true) && (this.state.printSize[i] === '')) {
                    alert("Please fill in the Printing Size in Suborder: " + (i + 1))
                    this.setState({loading: false});
                    return
                } else if (this.state.showTaxForm[i] === true && this.state.collection[i] === '') {
                    alert("Please fill in the Collection in Suborder: " + (i + 1))
                    this.setState({loading: false});
                    return
                }


            }
        }
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
    deleteSuborder = (index) => {
        let newSubOrderList = this.state.subOrderList.slice()
        newSubOrderList.splice(index, 1);
        for (var i = index; i < newSubOrderList.length; i++) {
            newSubOrderList[i]--;
        }
        this.setState({subOrderList: newSubOrderList})
        this.deleteSuborderValues(index, this.state.certified, "certified")
        this.deleteSuborderValues(index, this.state.deathPlace, "deathPlace")
        this.deleteSuborderValues(index, this.state.cemetery, "cemetery")
        this.deleteSuborderValues(index, this.state.firstName, "firstName")
        this.deleteSuborderValues(index, this.state.lastName, "lastName")
        this.deleteSuborderValues(index, this.state.birthPlace, "birthPlace")
        this.deleteSuborderValues(index, this.state.gender, "gender")
        this.deleteSuborderValues(index, this.state.fatherName, "fatherName")
        this.deleteSuborderValues(index, this.state.motherName, "motherName")
        this.deleteSuborderValues(index, this.state.middleName, "middleName")
        this.deleteSuborderValues(index, this.state.certificateNum, "certificateNum")
        this.deleteSuborderValues(index, this.state.groomLastName, "groomLastName")
        this.deleteSuborderValues(index, this.state.groomFirstName, "groomFirstName")
        this.deleteSuborderValues(index, this.state.brideLastName, "brideLastName")
        this.deleteSuborderValues(index, this.state.brideFirstName, "brideFirstName")
        this.deleteSuborderValues(index, this.state.month, "month")
        this.deleteSuborderValues(index, this.state.day, "day")
        this.deleteSuborderValues(index, this.state.year, "year")
        this.deleteSuborderValues(index, this.state.marriagePlace, "marriagePlace")
        this.deleteSuborderValues(index, this.state.letter, "letter")
        this.deleteSuborderValues(index, this.state.block, "block")
        this.deleteSuborderValues(index, this.state.lot, "lot")
        this.deleteSuborderValues(index, this.state.roll, "roll")
        this.deleteSuborderValues(index, this.state.borough, "borough")
        this.deleteSuborderValues(index, this.state.buildingNum, "buildingNum")
        this.deleteSuborderValues(index, this.state.street, "street")
        this.deleteSuborderValues(index, this.state.mail, "mail")
        this.deleteSuborderValues(index, this.state.contactNum, "contactNum")
        this.deleteSuborderValues(index, this.state.imgId, "imgId")
        this.deleteSuborderValues(index, this.state.imgTitle, "imgTitle")
        this.deleteSuborderValues(index, this.state.comment, "comment")
        this.deleteSuborderValues(index, this.state.personalUseAgreement, "personalUseAgreement")
        this.deleteSuborderValues(index, this.state.addDescription, "addDescription")
        this.deleteSuborderValues(index, this.state.collection, "collection")
        this.deleteSuborderValues(index, this.state.printSize, "printSize")
        this.deleteSuborderValues(index, this.state.numCopies, "numCopies")
        this.deleteSuborderValues(index, this.state.orderType, "orderType")
        this.deleteSuborderValues(index, this.state.status, "status")
        this.deleteSuborderValues(index, this.state.showMarriageSearch, "showMarriageSearch")
        this.deleteSuborderValues(index, this.state.showBirthSearch, "showBirthSearch")
        this.deleteSuborderValues(index, this.state.showBirthCert, "showBirthCert")
        this.deleteSuborderValues(index, this.state.showMarriageCert, "showMarriageCert")
        this.deleteSuborderValues(index, this.state.showDeathCert, "showDeathCert")
        this.deleteSuborderValues(index, this.state.showDeathSearch, "showDeathSearch")
        this.deleteSuborderValues(index, this.state.showTaxForm, "showTaxForm")
        this.deleteSuborderValues(index, this.state.showPhotoGalleryForm, "showPhotoGalleryForm")
        this.deleteSuborderValues(index, this.state.showPropertyForm, "showPropertyForm")
        this.index--;
        console.log(this.state)
    };

    render() {
        console.log('current list is ' + this.state.subOrderList);
        const SubOrders = this.state.subOrderList.map((suborderIndex) =>
            <Segment color={'black'} compact key={suborderIndex.toString()}>
                <SubOrderForm
                    key={suborderIndex}
                    index={suborderIndex}
                    callBack={this.callBack}
                    state={this.state}
                    ref={instance => {
                        this.subOrderForm = instance
                    }}
                    deleteSuborder={this.deleteSuborder}

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
                                    <Container>

                                        <Segment.Group compact>
                                            {SubOrders}
                                        </Segment.Group>
                                    </Container>
                                    <Button animated positive type="button" floated="left" onClick={() => {
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
                                    <Button type="reset" negative onClick={() => {
                                        this.clearSelection()
                                        this.subOrderForm.clearSelection()
                                    }} content="Clear"/>
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
    }
    ;
}

export default NewOrderForm;