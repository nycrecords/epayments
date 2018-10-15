/**
 * Created by sinsang on 4/25/17.
 */
import React from 'react';
import {Form, Menu, Button, Container, Segment} from 'semantic-ui-react';
import Date from './datepicker'
import 'react-datepicker/dist/react-datepicker.css'
import 'semantic-ui-css/semantic.min.css';
import moment from 'moment';
import {csrfFetch, handleFetchErrors} from "../utils/fetch"
import {CHUNK_SIZE} from "../constants/constants"


//Creates the options for the Order Type dropdown.
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
    {key: 'multipleincart', text: 'Multiple Items In Cart', value: 'multiple_items'}
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

//Creates the Search Form for the left side of the website.
class OrderForm extends React.Component {
    constructor() {
        super();

        this.clearSelection = () => {
            this.setState({
                order_number: '',
                suborder_number: '',
                status: 'all',
                order_type: 'all',
                billing_name: '',
            });

            if (this.state.activeItem === "Date Received") {
                this.dateReceivedStart.setState({
                    date: null,
                });

                this.dateReceivedEnd.setState({
                    date: null,
                });
            }
            else {
                this.dateSubmittedStart.setState({
                    date: null,
                });

                this.dateSubmittedEnd.setState({
                    date: null,
                });
            }
        };

        this.state = {
            order_number: '',
            suborder_number: '',
            order_type: 'all',
            status: 'all',
            billing_name: '',
            activeItem: 'Date Received',
            start: 0,
            size: CHUNK_SIZE
        };

        this.photosValueList = ['photos', 'Tax Photo', 'Photo Gallery'];

        this.yesterday = moment().subtract(1, 'days');
        this.today = moment();

        const formatDate = (dateRef) => (
            dateRef && dateRef.state.date ? dateRef.state.date.format('MM/DD/YYYY') : ''
        );

        this.submitData = (e) => {
            e.preventDefault();
            this.setStartZero(e);
        };

        this.submitFormData = (e, print) => {
            // e.preventDefault();

            switch (print) {
                case 'orders':
                case 'large_labels':
                case 'small_labels':
                    csrfFetch('api/v1.0/print/' + print, {
                        method: "POST",
                        body: JSON.stringify({
                            order_number: this.state.order_number,
                            suborder_number: this.state.suborder_number,
                            order_type: this.state.order_type,
                            status: this.state.status,
                            billing_name: this.state.billing_name,
                            date_received_start: formatDate(this.dateReceivedStart),
                            date_received_end: formatDate(this.dateReceivedEnd),
                            date_submitted_start: formatDate(this.dateSubmittedStart),
                            date_submitted_end: formatDate(this.dateSubmittedEnd),
                            start: this.state.start,
                            size: this.state.size,
                        })
                    })
                        .then(handleFetchErrors)
                        .then((json) => {
                            this.props.setLoadingState(false);
                            window.open(json.url);
                        }).catch((error) => {
                        console.error(error);
                        this.props.setLoadingState(false);
                    });
                    break;

                case 'csv':
                    let params = {
                        order_number: this.state.order_number,
                        suborder_number: this.state.suborder_number,
                        order_type: this.state.order_type,
                        status: this.state.status,
                        billing_name: this.state.billing_name,
                        date_received_start: formatDate(this.dateReceivedStart),
                        date_received_end: formatDate(this.dateReceivedEnd),
                        date_submitted_start: formatDate(this.dateSubmittedStart),
                        date_submitted_end: formatDate(this.dateSubmittedEnd),
                        start: this.state.start,
                        size: this.state.size,
                    };

                    let esc = encodeURIComponent;
                    let query = Object.keys(params)
                        .map(k => esc(k) + '=' + esc(params[k]))
                        .join('&');
                    csrfFetch('api/v1.0/orders/csv?' + query)
                        .then(handleFetchErrors)
                        .then((json) => {
                            this.props.setLoadingState(false);
                            window.open(json.url);
                        }).catch((error) => {
                        console.error(error);
                        this.props.setLoadingState(false);
                    });
                    break;

                // Search
                case 'submit':
                    this.props.setLoadingState(true);
                    csrfFetch('api/v1.0/orders', {
                        method: "POST",
                        body: JSON.stringify({
                            order_number: this.state.order_number,
                            suborder_number: this.state.suborder_number,
                            order_type: this.state.order_type,
                            status: this.state.status,
                            billing_name: this.state.billing_name,
                            date_received_start: formatDate(this.dateReceivedStart),
                            date_received_end: formatDate(this.dateReceivedEnd),
                            date_submitted_start: formatDate(this.dateSubmittedStart),
                            date_submitted_end: formatDate(this.dateSubmittedEnd),
                            start: this.state.start,
                            size: this.state.size,

                        })
                    })
                        .then(handleFetchErrors)
                        .then((json) => {
                            this.props.addOrder(json.order_count, json.suborder_count, json.all_orders, true);
                            this.props.setLoadingState(false);
                        })
                        .catch((error) => {
                            console.error(error);
                            this.props.setLoadingState(false);
                        });
                    break;

                case 'load_more':
                    this.props.setLoadingState(true);
                    csrfFetch('api/v1.0/orders', {
                        method: "POST",
                        body: JSON.stringify({
                            order_number: this.state.order_number,
                            suborder_number: this.state.suborder_number,
                            order_type: this.state.order_type,
                            status: this.state.status,
                            billing_name: this.state.billing_name,
                            date_received_start: formatDate(this.dateReceivedStart),
                            date_received_end: formatDate(this.dateReceivedEnd),
                            date_submitted_start: formatDate(this.dateSubmittedStart),
                            date_submitted_end: formatDate(this.dateSubmittedEnd),
                            start: this.state.start,
                            size: this.state.size,

                        })
                    })
                        .then(handleFetchErrors)
                        .then((json) => {
                            this.props.addOrder(json.order_count, json.suborder_count, json.all_orders, false);
                            this.props.setLoadingState(false);
                        })
                        .catch((error) => {
                            console.error(error);
                            this.props.setLoadingState(false);
                        });
                    break;
                // no default
            }
        };

        this.setStartZero = (e) => {
            this.setState({
                start: 0,
            }, () => this.submitFormData(e, 'submit'));
        };

        this.setStartSize = (e) => {
            this.setState({
                start: this.state.start + CHUNK_SIZE
            }, () => this.submitFormData(e, 'load_more'));
        };
    }

    handleItemClick = (e, {name}) => this.setState({activeItem: name});

    render() {
        const {activeItem} = this.state;
        return (
            <Container>
                <Form onSubmit={this.submitData}>
                    {/*This component defines the form fields required for the search form:

                         The Order Number, Suborder Number, Order Type, Billing Name, Date Received/Submitted Start and End.
                         Order Number, Suborder Number, and Billing Name are input fields.
                         Order Type is a dropdown listing the types of orders requested
                         Date Received/Submitted Start and End are input fields that call the React Datepicker component
                         */}

                    <Form.Input label="Order Number" placeholder="Order Number" maxLength="64"
                                onChange={(e, {value}) => {
                                    if (/^[0-9]+$/.test(value.slice(-1)) || value === '') {
                                        this.setState({order_number: value})
                                    }
                                }}
                                value={this.state.order_number}
                                className="margin-small-tb"
                    />

                    <Form.Input label="Suborder Number" placeholder="Suborder Number" maxLength="32"
                                onChange={(e, {value}) => {
                                    if (/^[\d -]+$/.test(value.slice(-1)) || value === '') {
                                        this.setState({suborder_number: value})
                                    }
                                }}
                                value={this.state.suborder_number}
                                className="margin-small-tb"
                    />
                    <Form.Select label="Order Type" placeholder="Order Type" options={orderTypeOptions}
                                 onChange={(e, {value}) => {
                                     this.setState({order_type: value});

                                     // Toggle visibility of "Generate CSV" button
                                     (this.photosValueList.indexOf(value) > -1) ? this.props.toggleCSV(true) : this.props.toggleCSV(false);
                                 }}
                                 value={this.state.order_type}
                                 className="margin-small-tb"
                    />
                    <Form.Select label="Status" placeholder="Status" options={statusOptions}
                                 onChange={(e, {value}) => {
                                     this.setState({status: value})
                                 }}
                                 value={this.state.status}
                                 className="margin-small-tb"
                    />
                    <Form.Input label="Billing Name" placeholder="Billing Name" maxLength="64"
                                onChange={(e, {value}) => {
                                    if (/^[a-zA-Z\s]*$/.test(value.slice(-1)) || value === '') {
                                        this.setState({billing_name: value})
                                    }
                                }}
                                value={this.state.billing_name}
                                className="margin-small-tb"
                    />

                    <Menu pointing attached='top' borderless>
                        <Menu.Item
                            name='Date Received'
                            active={activeItem === 'Date Received'}
                            onClick={this.handleItemClick}
                        />

                        <Menu.Item position='right'
                                   name="Date Submitted"
                                   active={activeItem === 'Date Submitted'}
                                   onClick={this.handleItemClick}
                        />
                    </Menu>
                    <Segment attached="bottom">
                        <Form.Group>
                            <Form.Field>
                                <Date
                                    label="Start"
                                    name="Start"
                                    maxDate={this.today}
                                    date={this.today}
                                    ref={
                                        (date) => {
                                            if (activeItem === 'Date Submitted') {
                                                return this.dateSubmittedStart = date
                                            }
                                            else {
                                                return this.dateReceivedStart = date
                                            }
                                        }}
                                    className="margin-small-tb"
                                />
                            </Form.Field>
                        </Form.Group>
                        <Form.Group>
                            <Form.Field>
                                <Date
                                    label="End"
                                    name="End"
                                    maxDate={this.today}
                                    ref={
                                        (date) => {
                                            if (activeItem === 'Date Submitted') {
                                                return this.dateSubmittedEnd = date
                                            }
                                            else {
                                                return this.dateReceivedEnd = date
                                            }
                                        }}
                                    className="margin-small-tb"
                                />
                            </Form.Field>
                        </Form.Group>
                    </Segment>
                    <Button type="reset" onClick={this.clearSelection} content="Clear"/>
                    <Button type='submit' positive floated="right" content="Apply"/>
                </Form>
            </Container>
        )
    }
}

export default OrderForm
