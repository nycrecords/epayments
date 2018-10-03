import React from 'react';
import {Link} from 'react-router-dom';
import {Button, Container, Dimmer, Divider, Form, Grid, Header, Icon, Loader, Segment,} from 'semantic-ui-react';
import swal from 'sweetalert';
import {csrfFetch, handleFetchErrors} from "../utils/fetch";
import NewSuborderForm from "./newSuborderForm";

class NewOrderForm extends React.Component {
    constructor() {
        super();

        this.state = {
            orderInfo: {
                billingName: '',
                email: '',
                addressLine1: '',
                addressLine2: '',
                city: '',
                state: '',
                zipCode: '',
                phone: ''
            },
            loading: false,
            suborderList: [{key: 0}]
        };
        this.handleChange = this.handleChange.bind(this);
        this.clearSelection = () => {
            swal("Clearing Form", "Are you sure you want to do this?", "warning", {
                buttons: {
                    no: {
                        text: "No",
                        value: false,
                    },
                    yes: {
                        text: "Yes",
                        value: true,
                    },
                },
            })
                .then((value) => {
                    if (value === false) {
                        // return;
                    }
                    else {
                        this.index = 1;
                        this.setState({
                            orderInfo: {
                                billingName: '',
                                email: '',
                                addressLine1: '',
                                addressLine2: '',
                                city: '',
                                state: '',
                                zipCode: '',
                                phone: ''
                            },
                            loading: false,
                            suborderList: [{key: 0, numCopies: 1}],
                        });
                        this.newSuborderForm.clearSelection();
                    }
                });
        };

        this.index = 1;
        this.message = "";
        this.vitalRecordTypes = ['Birth Cert', 'Death Cert', 'Marriage Cert'];
        this.vrpRequiredFields = ['year']
    };

    handleSuborderListChange = (name, value, key) => {
        let index = this.state.suborderList.findIndex((suborder) => {
            return suborder.key === key;
        });
        this.setState(prevState => {
            const newItems = [...prevState.suborderList];
            newItems[index][name] = value;
            return {suborderList: newItems}
        });
    };

    handleChange = (e) => {
        this.setState({
            orderInfo: {
                ...this.state.orderInfo,
                [e.target.name]: e.target.value
            }
        });
    };

    handleClick = () => {
        this.setState({suborderList: this.state.suborderList.concat({key: this.index})});
        this.index++;
    };

    handleSubmit = (e, value) => {
        e.preventDefault();
        this.setState({loading: true});

        for (let i = 0; i < this.state.suborderList.length; i++) {
            let orderType = this.state.suborderList[i].orderType;
            if (!orderType) {
                this.message += ("Please fill in Order Type in Suborder: " + (i + 1) + "\n");
            }
            else {
                if (this.vitalRecordTypes.indexOf(orderType) > -1) {
                    if (orderType === 'Marriage Cert') {
                        if (!this.state.suborderList[i].groomLastName) {
                            this.message += ("Please fill in the Last Name of Bride/Groom/Spouse 1 in Suborder: " + (i + 1) + "\n")
                        }

                        if (!this.state.suborderList[i].brideLastName) {
                            this.message += ("Please fill in the Last Name of Bride/Groom/Spouse 2 in Suborder: " + (i + 1) + "\n")
                        }
                    }
                    else {
                        if (!this.state.suborderList[i].lastName) {
                            this.message += ("Please fill in the Last Name in Suborder: " + (i + 1) + "\n")
                        }
                    }

                    let yearsArray = this.state.suborderList[i].years;
                    if (!yearsArray || !yearsArray[0].value) {
                        this.message += ("Please fill in the Year in Suborder: " + (i + 1) + "\n")
                    }

                    let boroughArray = this.state.suborderList[i].borough;
                    if (!boroughArray || !boroughArray.some(borough => borough.checked === true)) {
                        this.message += ("Please choose at least one Borough in Suborder: " + (i + 1) + "\n")
                    }

                    if (!this.state.suborderList[i].deliveryMethod) {
                        this.message += ("Please choose a Delivery Method in Suborder: " + (i + 1) + "\n")
                    }
                }

                else if (orderType === 'Tax Photo') {
                    if (!this.state.suborderList[i].collection) {
                        this.message += ("Please choose a Collection in Suborder: " + (i + 1) + "\n")
                    }

                    if (!this.state.suborderList[i].borough) {
                        this.message += ("Please choose a Borough in Suborder: " + (i + 1) + "\n")
                    }

                    if (!this.state.suborderList[i].buildingNum) {
                        this.message += ("Please fill in the Building Number in Suborder: " + (i + 1) + "\n")
                    }

                    if (!this.state.suborderList[i].street) {
                        this.message += ("Please fill in the Street in Suborder: " + (i + 1) + "\n")
                    }

                    if (!this.state.suborderList[i].size) {
                        this.message += ("Please choose a Size in Suborder: " + (i + 1) + "\n")
                    }

                    let deliveryMethod = this.state.suborderList[i].deliveryMethod;
                    if (!deliveryMethod) {
                        this.message += ("Please choose a Delivery Method in Suborder: " + (i + 1) + "\n")
                    }
                    else {
                        if (deliveryMethod === 'pickup' && !this.state.suborderList[i].contactNum) {
                            this.message += ("Please fill in the Contact Number in Suborder: " + (i + 1) + "\n")
                        }
                    }
                }

                else if (orderType === 'Photo Gallery') {
                    if (!this.state.suborderList[i].imageID) {
                        this.message += ("Please fill in the Image Identifier in Suborder: " + (i + 1) + "\n")
                    }

                    if (!this.state.suborderList[i].size) {
                        this.message += ("Please choose a Size in Suborder: " + (i + 1) + "\n")
                    }

                    let deliveryMethod = this.state.suborderList[i].deliveryMethod;
                    if (!deliveryMethod) {
                        this.message += ("Please choose a Delivery Method in Suborder: " + (i + 1) + "\n")
                    }
                    else {
                        if (deliveryMethod === 'pickup' && !this.state.suborderList[i].contactNum) {
                            this.message += ("Please fill in the Contact Number in Suborder: " + (i + 1) + "\n")
                        }
                    }
                }

                if (!this.state.suborderList[i].status) {
                    this.message += ("Please fill in Status in Suborder: " + (i + 1) + "\n");
                }

                if (!this.state.suborderList[i].numCopies) {
                    this.message += ("Please fill in Status in Suborder: " + (i + 1) + "\n");
                }
            }

            if (this.message.length > 0) {
                swal("Incomplete Form Submission", this.message, "error");
                this.message = "";
                this.setState({loading: false});
                return;
            }
        }

        csrfFetch('api/v1.0/orders/new', {
            method: "POST",
            body: JSON.stringify({
                orderInfo: this.state.orderInfo,
                suborderList: this.state.suborderList
            })
        })
            .then(handleFetchErrors)
            .then((json) => {
                // TODO: clear state?
                this.index = 1;
                this.setState({
                    orderInfo: {
                        billingName: '',
                        email: '',
                        addressLine1: '',
                        addressLine2: '',
                        city: '',
                        state: '',
                        zipCode: '',
                        phone: ''
                    },
                    loading: false,
                    suborderList: [{key: 0, numCopies: 1}],
                });
                this.newSuborderForm.clearSelection();
                // this.setState({loading: false});
                // window.open(json.url);

            }).catch((error) => {
            console.error(error);
            this.setState({loading: false});
        });
        swal("Thank you", "Your order has been submitted", "success");
    }
    ;

    deleteSuborder = (index) => {
        let newSuborderList = this.state.suborderList.filter((val) => {
            return val.key !== index
        });
        this.setState({suborderList: newSuborderList});
    };

    clearStateOnOrderTypeChange = (key) => {
        // This function resets the order's suborderList values when order type is changed
        let index = this.state.suborderList.findIndex((suborder) => {
            return suborder.key === key;
        });
        this.setState(prevState => {
            const newItems = [...prevState.suborderList];
            newItems[index] = {key: key, numCopies: 1};
            // newItems[index]['suborderList'] = {key: key};
            return {suborderList: newItems}
        });
    };

    render() {
        const Suborders = this.state.suborderList.map((suborder, i) =>
            <NewSuborderForm
                key={suborder.key}
                suborderKey={suborder.key}
                index={i}
                ref={instance => {
                    this.newSuborderForm = instance
                }}
                handleSuborderListChange={this.handleSuborderListChange}
                deleteSuborder={this.deleteSuborder}
                clearStateOnOrderTypeChange={this.clearStateOnOrderTypeChange}
            />
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
                            <Grid.Column width={3}>
                                <Form onSubmit={this.handleSubmit}>
                                    <Form.Input label="Billing Name"
                                                required
                                                name="billingName"
                                                placeholder="Billing Name"
                                                maxLength="64"
                                                onChange={this.handleChange}
                                                value={this.state.orderInfo.billingName}
                                    />
                                    <Form.Input label="Email"
                                                required
                                                name="email"
                                                placeholder="Email"
                                                maxLength="64"
                                                onChange={this.handleChange}
                                                value={this.state.orderInfo.email}
                                    />
                                    <Form.Input label="Address line 1"
                                                name="addressLine1"
                                                placeholder="Address"
                                                maxLength="64"
                                                onChange={this.handleChange}
                                                value={this.state.orderInfo.addressLine1}
                                    />
                                    <Form.Input label="Address line 2"
                                                name="addressLine2"
                                                placeholder="Address"
                                                maxLength="64"
                                                onChange={this.handleChange}
                                                value={this.state.orderInfo.addressLine2}
                                    />

                                    <Form.Input label="City"
                                                name="city"
                                                placeholder="City"
                                                maxLength="64"
                                                onChange={this.handleChange}
                                                value={this.state.orderInfo.city}
                                    />
                                    <Form.Input label="State"
                                                name="state"
                                                placeholder="State"
                                                maxLength="64"
                                                onChange={this.handleChange}
                                                value={this.state.orderInfo.state}
                                    />
                                    <Form.Input label="Zip Code"
                                                name="zipCode"
                                                placeholder="Zip Code"
                                                maxLength="5"
                                                onChange={this.handleChange}
                                                value={this.state.orderInfo.zipCode}
                                    />

                                    <Form.Input label="Phone"
                                                name="phone"
                                                placeholder="Phone"
                                                maxLength="64"
                                                onChange={this.handleChange}
                                                value={this.state.orderInfo.phone}
                                    />
                                    <Button animated positive type="button" floated="left" onClick={() => {
                                        this.handleClick();
                                        this.addSuborder.scrollIntoView({
                                            block: "end",
                                            behavior: "smooth",
                                        });
                                        this.addSuborder.scrollTop = this.addSuborder.scrollHeight;
                                    }}>
                                        <Button.Content visible>
                                            <Icon name='add'/>
                                        </Button.Content>
                                        <Button.Content hidden>
                                            Additional Order
                                        </Button.Content>
                                    </Button>
                                    <Button type='submit' positive floated="left" content="Place Order"/>
                                    <Button type="reset" negative onClick={this.clearSelection} content="Clear"/>
                                </Form>
                                <strong>Number of Suborders: {this.state.suborderList.length}</strong>
                            </Grid.Column>
                            <Grid.Column width={7} id="grid-column-order">
                                <div ref={(el) => {
                                    this.addSuborder = el;
                                }}>
                                    <Form>
                                        <Segment.Group>
                                            {Suborders}
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
