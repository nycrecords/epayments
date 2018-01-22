/**
 * Created by sinsang on 4/25/17.
 */
import React from 'react';
import {Form, Button, Container} from 'semantic-ui-react';
import Date from './datepicker'
import 'react-datepicker/dist/react-datepicker.css'
import 'semantic-ui-css/semantic.min.css';
import moment from 'moment';
import {csrfFetch} from "../utils/fetch"


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
    {key: 'phototax', text: 'Photo Tax', value: 'Photo Tax'},
    {key: 'photogallery', text: 'Photo Gallery', value: 'Photo Gallery'},
    {key: 'other', text: '--Other--', value: 'other'},
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

//Creates the Search Form for the left side of the website.
class OrderForm extends React.Component {
    constructor() {
        super();

        this.clearSelection = () => {
            this.setState({
                ordernumber: '',
                subordernumber: '',
                status: '',
                order_type: '',
                billing_name: '',
            });

            this.dateSubmittedStart.setState({
                date: '',
            });


            this.dateSubmittedEnd.setState({
                date: '',
            });
        };

        this.state = {
            ordernumber: '',
            subordernumber: '',
            order_type: '',
            status: 'all',
            billing_name: ''

        };

        this.yesterday = moment().subtract(1, 'days');
        this.today = moment()

        const formatDate = (dateRef) => (
            dateRef && dateRef.state.date ? dateRef.state.date.format('MM/DD/YYYY') : ''
        );

        this.submitFormData = (e, print) => {
            e.preventDefault();
            if (print === undefined) {
                this.props.setLoadingState(true);
                csrfFetch('api/v1.0/orders', {
                    method: "POST",
                    body: JSON.stringify({
                        order_number: this.state.ordernumber,
                        suborder_number: this.state.subordernumber,
                        order_type: this.state.order_type,
                        status: this.state.status,
                        billing_name: this.state.billing_name,
                        date_submitted_start: formatDate(this.dateSubmittedStart),
                        date_submitted_end: formatDate(this.dateSubmittedEnd)
                    })
                }).then((response) => {
                    return response.json();
                }).then((json) => {
                    this.props.addOrder(json.order_count, json.suborder_count, json.all_orders);
                    this.props.setLoadingState(false);
                });
            }
            else {
                csrfFetch('api/v1.0/print/' + print, {
                    method: "POST",
                    body: JSON.stringify({
                        order_number: this.state.ordernumber,
                        suborder_number: this.state.subordernumber,
                        order_type: this.state.order_type,
                        status: this.state.status,
                        billing_name: this.state.billing_name,
                        date_submitted_start: formatDate(this.dateSubmittedStart),
                        date_submitted_end: formatDate(this.dateSubmittedEnd)
                    })
                }).then((response) => {
                    return response.json();
                }).then((json) => {
                    this.props.setLoadingState(false);
                    window.open(json.url);
                })
            }
        };
    }

    render() {
        return (
            <Container>
                <Form onSubmit={this.submitFormData}>
                    {/*This component defines the form fields required for the search form:

                         The Order Number, Suborder Number, Order Type, Billing Name, Date Received Start and End.
                         Order Number, Suborder Number, and Billing Name are input fields.
                         Order Type is a dropdown listing the types of orders requested
                         Date Received Start and End are input fields that call the React Datepicker component
                         */}

                    <Form.Input label="Order Number" placeholder="Order Number" maxLength="64"
                                onChange={(e, {value}) => {
                                    if (/^[0-9]+$/.test(value.slice(-1)) || value === '') {
                                        this.setState({ordernumber: value})
                                    }
                                }}
                                value={this.state.ordernumber}
                    />

                    <Form.Input label="Suborder Number" placeholder='Suborder Number' maxLength="32"
                                onChange={(e, {value}) => {
                                    if (/^[\d -]+$/.test(value.slice(-1)) || value === '') {
                                        this.setState({subordernumber: value})
                                    }
                                }}
                                value={this.state.subordernumber}

                    />
                    <Form.Select label="Order Type" placeholder="Order Type" options={orderTypeOptions}
                                 onChange={(e, {value}) => {
                                     this.setState({order_type: value})
                                 }}
                                 value={this.state.order_type}
                    />
                    <Form.Select label="Status" placeholder="Status" options={statusOptions}
                                 onChange={(e, {value}) => {
                                     this.setState({status: value})
                                 }}
                                 value={this.state.status}
                    />
                    <Form.Input label="Billing Name" placeholder="Billing Name" maxLength="64"
                                onChange={(e, {value}) => {
                                    if (/^[a-zA-Z\s]*$/.test(value.slice(-1)) || value === '') {
                                        this.setState({billing_name: value})
                                    }
                                }}
                                value={this.state.billing_name}
                    />

                    <Form.Group>
                        <Form.Field width="16">
                            <Date
                                label="Date Submitted - Start"
                                name="Date Submitted - Start"
                                date={this.today}
                                maxDate={this.today}
                                ref={(date) => this.dateSubmittedStart = date}
                            />

                        </Form.Field>
                    </Form.Group>
                    <Form.Group>
                        <Form.Field width="16">
                            <Date
                                label="Date Submitted - End"
                                name="Date Submitted - End"
                                maxDate={this.today}
                                ref={(date) => this.dateSubmittedEnd = date}
                            />
                        </Form.Field>
                    </Form.Group>
                    <Button type="reset" onClick={this.clearSelection} content="Clear"/>
                    <Button type='submit' positive floated="right" content="Apply"/>
                </Form>
            </Container>
        )
    }
}

export default OrderForm

