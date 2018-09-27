import React, {} from 'react';
import {Link} from 'react-router-dom';
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
                            suborderList: [{key: 0}],
                        });
                        this.subOrderForm.clearSelection();
                    }
                });
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
        this.message = "";
        this.orderList = ['Tax Photo', 'Photo Gallery', 'Property Card', 'Marriage Search',
            'Marriage Cert', 'Death Search', 'Death Cert', 'Birth Search', 'Birth Cert'];
    };

    handleSuborderListChange = (name, value, index) => {
        console.log(this.state.suborderList);
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
        // TODO: check validation
        // for (var i = 0; i < this.state.suborderList.length; i++) {
        //     if (this.state.orderType[i] === '') {
        //         this.message += ("Please fill in Order Type in Suborder: " + (i + 1) + "\n");
        //     }
        //     if (this.state.status[i] === '') {
        //         this.message += ("Please fill in Status in Suborder: " + (i + 1) + "\n");
        //     }
        //     if (this.state.orderType[i] !== '') {
        //         if ((this.state.showBirthSearch[i] === true || this.state.showBirthCert === true[i]) && this.state.gender[i] === '') {
        //             this.message += ("Please fill in the Gender in Suborder: " + (i + 1) + "\n");
        //         }
        //         if (this.state.showPhotoGalleryForm[i] === false && this.state.borough[i] === '') {
        //             this.message += ("Please fill in the Borough in Suborder:" + (i + 1) + "\n");
        //         }
        //         if ((this.state.showPhotoGalleryForm[i] === true || this.state.showTaxForm[i] === true) && (this.state.printSize[i] === '')) {
        //             this.message += ("Please fill in the Printing Size in Suborder: " + (i + 1) + "\n")
        //         }
        //         if (this.state.showTaxForm[i] === true && this.state.collection[i] === '') {
        //             this.message += ("Please fill in the Collection in Suborder: " + (i + 1) + "\n");
        //         }
        //     }
        // }
        //
        // if (this.message.length !== 0) {
        //     swal("Incomplete Form Submission", this.message, "error");
        //     this.message = "";
        //     this.setState({loading: false});
        //     return;
        // }

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
                this.setState({loading: false});
                window.open(json.url);

            }).catch((error) => {
            console.error(error);
            this.setState({loading: false});
        });
        swal("Thank you", "Your order has been submitted", "success");
    };

    deleteSuborder = (index) => {
        debugger;
        let newSuborderList = this.state.suborderList.filter((val) => {return val.key != index});
        // let newSuborderList = this.state.suborderList.slice();

        // newSuborderList.splice(index, 1);
        // for (let i = index; i < newSuborderList.length; i++) {
        //     if (newSuborderList[i].key > index) {
        //         newSuborderList[i].key--;
        //     }
        // }
        this.setState({suborderList: newSuborderList});
        // this.index--;
    };

    render() {
        const SubOrders = this.state.suborderList.map((suborder) =>
            <SubOrderForm
                    key={suborder.key}
                    index={suborder.key}
                    // state={this.state}
                    ref={instance => {
                        this.subOrderForm = instance
                    }}
                    handleSuborderListChange={this.handleSuborderListChange}
                    deleteSuborder={this.deleteSuborder}
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