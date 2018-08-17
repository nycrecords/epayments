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
import swal from 'sweetalert';
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
            state: '',
            zipCode: '',
            phone: '',
            instructions: '',
            /**
             * I changed all list/array states to be nested in order to iterate to update state
             *      using Object.keys(this.state.suborder).map => //function//
             * child state now calls { this.props.state.suborder.[stateName] } instead of
             *      [this.props.state.[stateName]
             * fully working verison is Fri Aug 17 10:11:58 2018 -0400 1f91302 name changes  [jchen249]
             *      or the one before
             */
            suborder: {
                certified: [''],
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
                block: [''],
                lot: [''],
                roll: [''],
                borough: [''],
                buildingNum: [''],
                street: [''],
                contactNum: [''],
                imgId: [''],
                imgTitle: [''],
                comment: [''],
                addDescription: [''],
                collection: [''],
                printSize: [''],
                numCopies: [''],
                status: [''],
                letter: [false],
                personalUseAgreement: [false],
                mail: [false],
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
            },
            loading: false,
            subOrderList: [0]
        };
        this.handleChange = this.handleChange.bind(this);
        this.clear = () => {
            this.index = 1;
            this.setState({
                billingName: '',
                email: '',
                addressLine1: '',
                addressLine2: '',
                city: '',
                state: '',
                zipCode: '',
                phone: '',
                // birthPlace: [''],
                // cemetery: [''],
                // certified: [''],
                // deathPlace: [''],
                // fatherName: [''],
                // firstName: [''],
                // gender: [''],
                // instructions: '',
                // lastName: [''],
                // motherName: [''],
                // middleName: [''],
                // orderType: [''],
                // certificateNum: [''],
                // groomLastName: [''],
                // groomFirstName: [''],
                // brideLastName: [''],
                // brideFirstName: [''],
                // month: [''],
                // day: [''],
                // year: [''],
                // marriagePlace: [''],
                // letter: [''],
                // block: [''],
                // lot: [''],
                // roll: [''],
                // borough: [''],
                // buildingNum: [''],
                // street: [''],
                // contactNum: [''],
                // imgId: [''],
                // imgTitle: [''],
                // comment: [''],
                // addDescription: [''],
                // collection: [''],
                // printSize: [''],
                // numCopies: [''],
                // status: [''],
                // personalUseAgreement: [false],
                // mail: [false],
                // showBirthCert: [false],
                // showBirthSearch: [false],
                // showDeathCert: [false],
                // showDeathSearch: [false],
                // showMarriageCert: [false],
                // showMarriageSearch: [false],
                // showTaxForm: [false],
                // showPhotoGalleryForm: [false],
                // showPropertyForm: [false],
                subOrderList: [0],
            });
            // console.log(Object.keys(this.state.suborder));
            /**
             * tested with console.log(this.state.suborder)
             * and input checking
             **/
            Object.keys(this.state.suborder)
                .map((key, index) => {
                        if (typeof(this.state.suborder[key][0]) !== "boolean") {
                            this.setState({suborder: {...this.state.suborder, [key]: ['']}});
                        } else {
                            this.setState({suborder: {...this.state.suborder, [key]: [false]}});
                        }
                    }
                )


        };
        this.clearSelection = () => {
            swal("Clearing Form", "Are you sure you want to do this?", "warning", {
                buttons: {
                    no: {
                        text: "No",
                        value: "no",
                    },
                    yes: {
                        text: "Yes",
                        value: true,
                    },
                },
            })
                .then((value) => {
                    if (value === "no") {
                        return;
                    }
                    else {
                        this.clear();

                    }
                });
        };

        this.handleEmptyStates = () => {
            /*Add empty index to list whenever additional suborders are prompted
             to prevent null insert into DB if user left some fields unanswered
            */
            /**
             * adds empty string or false(boolean) onto exisitng state list
             * only works for showPropertyFrom state for now
             */
            Object.keys(this.state.suborder)
                .map((key) => {
                        let newKey = this.state.suborder[key].slice();
                        console.log(this.state.suborder[key][0]);
                        if (typeof(this.state.suborder[key][0]) !== "boolean") {
                            newKey = newKey.concat([""]);
                            this.setState({suborder: {...this.state.suborder, [key]: newKey}});
                        } else {
                            // debugger;
                            newKey = newKey.concat([false]);
                            this.setState({suborder: {...this.state.suborder, [key]: newKey}});
                        }
                    }
                )
            console.log(this.state.suborder)
            // this.setState({
            //     certified: this.state.certified.concat(['']),
            //     deathPlace: this.state.deathPlace.concat(['']),
            //     cemetery: this.state.cemetery.concat(['']),
            //     firstName: this.state.firstName.concat(['']),
            //     lastName: this.state.lastName.concat(['']),
            //     birthPlace: this.state.birthPlace.concat(['']),
            //     gender: this.state.gender.concat(['']),
            //     fatherName: this.state.fatherName.concat(['']),
            //     motherName: this.state.motherName.concat(['']),
            //     middleName: this.state.middleName.concat(['']),
            //     certificateNum: this.state.certificateNum.concat(['']),
            //     groomLastName: this.state.groomLastName.concat(['']),
            //     groomFirstName: this.state.groomFirstName.concat(['']),
            //     brideLastName: this.state.brideLastName.concat(['']),
            //     brideFirstName: this.state.brideFirstName.concat(['']),
            //     month: this.state.month.concat(['']),
            //     day: this.state.day.concat(['']),
            //     year: this.state.year.concat(['']),
            //     marriagePlace: this.state.marriagePlace.concat(['']),
            //     letter: this.state.letter.concat([false]),
            //     block: this.state.block.concat(['']),
            //     lot: this.state.lot.concat(['']),
            //     roll: this.state.roll.concat(['']),
            //     borough: this.state.borough.concat(['']),
            //     buildingNum: this.state.buildingNum.concat(['']),
            //     street: this.state.street.concat(['']),
            //     mail: this.state.mail.concat([false]),
            //     contactNum: this.state.contactNum.concat(['']),
            //     imgId: this.state.imgId.concat(['']),
            //     imgTitle: this.state.imgTitle.concat(['']),
            //     comment: this.state.comment.concat(['']),
            //     personalUseAgreement: this.state.personalUseAgreement.concat([false]),
            //     addDescription: this.state.addDescription.concat(['']),
            //     collection: this.state.collection.concat(['']),
            //     printSize: this.state.printSize.concat(['']),
            //     numCopies: this.state.numCopies.concat(['']),
            //     status: this.state.status.concat(['']),
            //     orderType: this.state.orderType.concat(['']),
            //     showMarriageSearch: this.state.showMarriageSearch.concat([false]),
            //     showBirthSearch: this.state.showBirthSearch.concat([false]),
            //     showBirthCert: this.state.showBirthCert.concat([false]),
            //     showMarriageCert: this.state.showMarriageCert.concat([false]),
            //     showDeathCert: this.state.showDeathCert.concat([false]),
            //     showDeathSearch: this.state.showDeathSearch.concat([false]),
            //     showTaxForm: this.state.showTaxForm.concat([false]),
            //     showPhotoGalleryForm: this.state.showPhotoGalleryForm.concat([false]),
            //     showPropertyForm: this.state.showPropertyForm.concat([false]),
            // })
        };
        this.deleteSuborderValues = (index, state, name) => {
            let newState = state.slice();
            newState.splice(index, 1);
            for (let i = index; i < newState; i++) {
                newState[i] = newState[i - 1]
            }
            this.setState({[name]: newState})
        };
        this.index = 1;
        this.message = "";
        this.orderList = ['Tax Photo', 'Photo Gallery', 'Property Card', 'Marriage Search',
            'Marriage Cert', 'Death Search', 'Death Cert', 'Birth Search', 'Birth Cert'];
    };

    handleChange = (e) => {
        const target = e.target;
        const value = target.value;
        const name = target.name;
        this.setState({
            [name]: value
        });
    };
    handleAddOrder = () => {
        this.setState({subOrderList: this.state.subOrderList.concat([this.index])});
        this.index++;
    };

    handleSubmit = (e, value) => {
        e.preventDefault();
        this.setState({loading: true});
        for (let i = 0; i < this.state.subOrderList.length; i++) {
            if (this.state.suborder.orderType[i] === '') {
                this.message += ("Please fill in Order Type in Suborder: " + (i + 1) + "\n");
            }
            if (this.state.suborder.status[i] === '') {
                this.message += ("Please fill in Status in Suborder: " + (i + 1) + "\n");
            }
            if (this.state.suborder.numCopies[i] === '') {
                this.message += ("Please fill in Number of Copies in Suborder: " + (i + 1) + "\n");
            }
            if (this.state.suborder.orderType[i] !== '') {
                if ((this.state.suborder.showBirthSearch[i] === true || this.state.suborder.showBirthCert[i] === true) &&
                    this.state.suborder.gender[i] === '') {
                    this.message += ("Please fill in the Gender in Suborder: " + (i + 1) + "\n");
                }
                if (this.state.suborder.year[i] === '' && this.state.suborder.showPhotoGalleryForm[i] === false &&
                    this.state.suborder.showPropertyForm[i] === false && this.state.suborder.showTaxForm[i] === false) {
                    this.message += ("Please fill in the Year in Suborder: " + (i + 1) + "\n");
                }
                if (this.state.suborder.showPhotoGalleryForm[i] === false && this.state.suborder.borough[i] === '') {
                    this.message += ("Please fill in the Borough in Suborder:" + (i + 1) + "\n");
                }
                if ((this.state.suborder.showPhotoGalleryForm[i] === true || this.state.suborder.showTaxForm[i] === true) &&
                    (this.state.suborder.printSize[i] === '')) {
                    this.message += ("Please fill in the Printing Size in Suborder: " + (i + 1) + "\n")
                }
                if (this.state.suborder.showTaxForm[i] === true && this.state.suborder.collection[i] === '') {
                    this.message += ("Please fill in the Collection in Suborder: " + (i + 1) + "\n");
                }
            }
        }
        if (this.message.length !== 0) {
            swal("Incomplete Form Submission", this.message, "error");
            this.message = "";
            this.setState({loading: false});
            return;

        }
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
                certified: this.state.suborder.certified,
                orderType: this.state.suborder.orderType,
                gender: this.state.suborder.gender,
                motherName: this.state.suborder.motherName,
                fatherName: this.state.suborder.fatherName,
                birthPlace: this.state.suborder.birthPlace,
                certificateNum: this.state.suborder.certificateNum,
                groomLastName: this.state.suborder.groomFirstName,
                groomFirstName: this.state.suborder.groomFirstName,
                brideLastName: this.state.suborder.brideLastName,
                brideFirstName: this.state.suborder.brideFirstName,
                month: this.state.suborder.month,
                day: this.state.suborder.day,
                year: this.state.suborder.year,
                marriagePlace: this.state.suborder.marriagePlace,
                letter: this.state.suborder.letter,
                deathPlace: this.state.suborder.deathPlace,
                cemetery: this.state.suborder.cemetery,
                firstName: this.state.suborder.firstName,
                middleName: this.state.suborder.middleName,
                lastName: this.state.suborder.lastName,
                block: this.state.suborder.block,
                lot: this.state.suborder.lot,
                roll: this.state.suborder.roll,
                borough: this.state.suborder.borough,
                buildingNum: this.state.suborder.buildingNum,
                street: this.state.suborder.street,
                mail: this.state.suborder.mail,
                contactNum: this.state.suborder.contactNum,
                imgId: this.state.suborder.imgId,
                imgTitle: this.state.suborder.imgTitle,
                comment: this.state.suborder.comment,
                personalUseAgreement: this.state.suborder.personalUseAgreement,
                addDescription: this.state.suborder.addDescription,
                collection: this.state.suborder.collection,
                printSize: this.state.suborder.printSize,
                numCopies: this.state.suborder.numCopies,
                status: this.state.suborder.status

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
        swal("Thank you", "Your order has been submitted", "success");
        this.clear()

    };
    callBack = (dataFromChild, value, index, state) => {
        //update state from child
        let newState = state.slice();
        newState[index] = value;
        // this.setState({
        //     [dataFromChild]: newState
        // });
        this.setState({suborder: {...this.state.suborder, [dataFromChild]: newState}});
        // console.log(this.state.suborder);


    };
    deleteSuborder = (index) => {
        let newSubOrderList = this.state.subOrderList.slice()
        newSubOrderList.splice(index, 1);
        for (let i = index; i < newSubOrderList.length; i++) {
            newSubOrderList[i]--;
        }
        this.setState({subOrderList: newSubOrderList});
        Object.keys(this.state.suborder)//.filter(key => (typeof(this.state.suborder[key][0])) !== "boolean")
            .map((key,) => {
                this.deleteSuborderValues(index,this.state.suborder[key], key);
                }
            )
        /**
         * does not work, maybe b/c handleEmpty does not work fully
         * */

        // this.deleteSuborderValues(index, this.state.certified, "certified");
        // this.deleteSuborderValues(index, this.state.deathPlace, "deathPlace");
        // this.deleteSuborderValues(index, this.state.cemetery, "cemetery");
        // this.deleteSuborderValues(index, this.state.firstName, "firstName");
        // this.deleteSuborderValues(index, this.state.lastName, "lastName");
        // this.deleteSuborderValues(index, this.state.birthPlace, "birthPlace");
        // this.deleteSuborderValues(index, this.state.gender, "gender");
        // this.deleteSuborderValues(index, this.state.fatherName, "fatherName");
        // this.deleteSuborderValues(index, this.state.motherName, "motherName");
        // this.deleteSuborderValues(index, this.state.middleName, "middleName");
        // this.deleteSuborderValues(index, this.state.certificateNum, "certificateNum");
        // this.deleteSuborderValues(index, this.state.groomLastName, "groomLastName");
        // this.deleteSuborderValues(index, this.state.groomFirstName, "groomFirstName");
        // this.deleteSuborderValues(index, this.state.brideLastName, "brideLastName");
        // this.deleteSuborderValues(index, this.state.brideFirstName, "brideFirstName");
        // this.deleteSuborderValues(index, this.state.month, "month");
        // this.deleteSuborderValues(index, this.state.day, "day");
        // this.deleteSuborderValues(index, this.state.year, "year");
        // this.deleteSuborderValues(index, this.state.marriagePlace, "marriagePlace");
        // this.deleteSuborderValues(index, this.state.letter, "letter");
        // this.deleteSuborderValues(index, this.state.block, "block");
        // this.deleteSuborderValues(index, this.state.lot, "lot");
        // this.deleteSuborderValues(index, this.state.roll, "roll");
        // this.deleteSuborderValues(index, this.state.borough, "borough");
        // this.deleteSuborderValues(index, this.state.buildingNum, "buildingNum");
        // this.deleteSuborderValues(index, this.state.street, "street");
        // this.deleteSuborderValues(index, this.state.mail, "mail");
        // this.deleteSuborderValues(index, this.state.contactNum, "contactNum");
        // this.deleteSuborderValues(index, this.state.imgId, "imgId");
        // this.deleteSuborderValues(index, this.state.imgTitle, "imgTitle");
        // this.deleteSuborderValues(index, this.state.comment, "comment");
        // this.deleteSuborderValues(index, this.state.personalUseAgreement, "personalUseAgreement");
        // this.deleteSuborderValues(index, this.state.addDescription, "addDescription");
        // this.deleteSuborderValues(index, this.state.collection, "collection");
        // this.deleteSuborderValues(index, this.state.printSize, "printSize");
        // this.deleteSuborderValues(index, this.state.numCopies, "numCopies");
        // this.deleteSuborderValues(index, this.state.orderType, "orderType");
        // this.deleteSuborderValues(index, this.state.status, "status");
        // this.deleteSuborderValues(index, this.state.showMarriageSearch, "showMarriageSearch");
        // this.deleteSuborderValues(index, this.state.showBirthSearch, "showBirthSearch");
        // this.deleteSuborderValues(index, this.state.showBirthCert, "showBirthCert");
        // this.deleteSuborderValues(index, this.state.showMarriageCert, "showMarriageCert");
        // this.deleteSuborderValues(index, this.state.showDeathCert, "showDeathCert");
        // this.deleteSuborderValues(index, this.state.showDeathSearch, "showDeathSearch");
        // this.deleteSuborderValues(index, this.state.showTaxForm, "showTaxForm");
        // this.deleteSuborderValues(index, this.state.showPhotoGalleryForm, "showPhotoGalleryForm");
        // this.deleteSuborderValues(index, this.state.showPropertyForm, "showPropertyForm");
        this.index--;
    };

    render() {
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
                                <Header as="h1" textAlign="center">
                                    <Link to="/">
                                        ePayments
                                        <Container className="sub header">Department of Records</Container>
                                    </Link>
                                </Header>
                            </Grid.Column>
                        </Grid.Row>

                        <Grid.Row centered>
                            <Grid.Column>
                                <Header as="h1" dividing textAlign="center">New Order</Header>
                            </Grid.Column>
                        </Grid.Row>

                        <Grid.Row centered>
                            <Grid.Column width={5}>
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
                                    <Button animated positive type="button" floated="left" onClick={() => {
                                        this.handleEmptyStates()
                                        this.handleAddOrder()
                                        this.addSuborder.scrollIntoView({
                                            block: "end",
                                            behavior: "smooth",
                                        });
                                        this.addSuborder.scrollTop = this.addSuborder.scrollHeight;
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
                                    }} content="Clear"/>
                                    <br/>
                                    <strong>Number of Suborders: {this.index}</strong>
                                </Form>
                            </Grid.Column>
                            <Grid.Column width={6} id="grid-column-order">
                                <div ref={(el) => {
                                    this.addSuborder = el;
                                }}>
                                    <Form>

                                        <Segment.Group>
                                            {SubOrders}
                                        </Segment.Group>
                                    </Form>
                                </div>

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