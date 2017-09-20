/**
 * Created by sinsang on 4/25/17.
 */
import React from 'react';
import {Form, Button, Container} from 'semantic-ui-react';
import Date from './datepicker'
import 'react-datepicker/dist/react-datepicker.css'
import 'semantic-ui-css/semantic.min.css';
import moment from 'moment';
// import ReactTooltip from 'react-tooltip'

//Creates the options for the Order Type dropdown.
const options = [
    {key: 'all', text: 'All', value: 'all'},
    {key: 'vitalrecords', text: '--Vital Records--', value: 'vital records'},
    {key: 'birthsearch', text: 'Birth Search', value: 'Birth search'},
    {key: 'marriagesearch', text: 'Marriage Search', value: 'Marriage search'},
    {key: 'deathsearch', text: 'Death Search', value: 'Death search'},
    {key: 'birthcert', text: 'Birth Certificate', value: 'Birth cert'},
    {key: 'marriagecert', text: 'Marriage Certificate', value: 'Marriage cert'},
    {key: 'deathcert', text: 'Death Certificate', value: 'Death cert'},
    {key: 'photos', text: '--Photos--', value: 'photos'},
    {key: 'propertytax', text: 'Property Tax', value: 'property tax'},
    {key: 'phototax', text: 'Photo Tax', value: 'photo tax'},
    {key: 'photogallery', text: 'Photo Gallery', value: 'photo gallery'},
    {key: 'other', text: '--Other--', value: 'other'},
    {key: 'multipleincart', text: 'Multiple Items In Cart', value: 'multiple items in cart'},
    {key: 'vitalincart', text: 'Vital Records And Photos In Cart', value: 'vital records and photos in cart'}
];

//Creates the Search Form for the left side of the website.
class OrderForm extends React.Component {
    constructor() {
        super();

        this.handleKeyPress = (event) => {
            if (event.key) {
                event.preventDefault();
                return false;
            }
        };

        this.clearSelection = () => {
            this.setState({
                ordernumber: '',
                subordernumber: '',
                order_type: '',
                billing_name: '',
            });

            this.dateReceivedStart.setState({
                date: '',
            });


            this.dateReceivedEnd.setState({
                date: '',
            });
        };

        this.state = {
            ordernumber: '',
            subordernumber: '',
            order_type: '',
            billing_name: ''

        };
         const formatDate = (dateRef) => (
            dateRef && dateRef.state.date ? dateRef.state.date.format('MM/DD/YYYY') : ''
         );

        // TODO: Implement CSRF token
        this.handleSubmit = (e) => {
            e.preventDefault();
            fetch('api/v1.0/orders', {
                method: "POST",
                body: JSON.stringify({
                    order_no: this.state.ordernumber,
                    suborder_no: this.state.subordernumber,
                    order_type: this.state.order_type,
                    billing_name: this.state.billing_name,
                    date_received: formatDate(this.date),
                    date_submitted: formatDate(this.date_2)
                })
            }).then((response) => {
                return response.json()
            }).then((json) => {
                this.props.addOrder();
            });
        };
    }

    render() {
        return (
            <Container>
                <Form onSubmit={this.handleSubmit}>
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

                    <Form.Input label="Suborder Number" placeholder='Suborder Number' maxLength="64"
                                onChange={(e, {value}) => {
                                    if (/^[0-9]+$/.test(value.slice(-1)) || value === '') {
                                        this.setState({subordernumber: value})
                                    }
                                }}
                                value={this.state.subordernumber}

                    />
                    <Form.Select label="Order Type" placeholder="Order Type" options={options}
                                 onChange={(e, {value}) => {
                                     this.setState({order_type: value})
                                 }

                                 }
                                 value={this.state.order_type}
                    />
                    {/*<Form.Field label="Billing Name" placeholder="Billing Name" maxLength="64" control="input"git />*/}
                    <Form.Input label="Billing Name" placeholder="Billing Name" maxLength="64"
                                onChange={(e, {value}) => {
                                    if (/^[a-z,A-Z]+$/.test(value.slice(-1)) || value === '') {
                                        this.setState({billing_name: value})
                                    }
                                }}
                                value={this.state.billing_name}
                    />

                    <Form.Group>
                        <Form.Field width="16">
                            <Date
                                label="Date Received - Start"
                                name="Date Received - Start"
                                maxDate={moment().startOf('day')}
                                ref={(date) => this.dateReceivedStart = date}
                            />

                        </Form.Field>
                    </Form.Group>
                    <Form.Group>
                        <Form.Field width="16">
                            <Date
                                label="Date Received - End"
                                name="Date Received - End"
                                maxDate={moment().startOf('day')}
                                ref={(date) => this.dateReceivedEnd = date}
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

