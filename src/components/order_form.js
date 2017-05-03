/**
 * Created by sinsang on 4/25/17.
 */
import React from 'react';
import {Form, Button, Container} from 'semantic-ui-react';
import Date from './datepicker';
import 'react-datepicker/dist/react-datepicker.css'
import 'semantic-ui-css/semantic.min.css';
import MaskedInput from 'react-text-mask';

//Creates the options for the Order Type dropdown.
const options = [
    {key: 'all', text: 'All', value: 'all'},
    {key: 'vitalrecords', text: '--Vital Records--', value: 'vital records'},
    {key: 'birthsearch', text: 'Birth Search', value: 'birth search'},
    {key: 'marriagesearch', text: 'Marriage Search', value: 'marriage search'},
    {key: 'deathsearch', text: 'Death Search', value: 'death search'},
    {key: 'birthcert', text: 'Birth Certificate', value: 'birth certificate'},
    {key: 'marriagecert', text: 'Marriage Certificate', value: 'marriage certificate'},
    {key: 'deathcert', text: 'Death Certificate', value: 'death certificate'},
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
    handleKeyPress = (event) => {
        if (event.key) {
            event.preventDefault();
            return false;
        }
    };

    render() {
        return (
            <Container>
                <div>
                    <Form>

                        {/*This component defines the form fields required for the search form:

                         The Order Number, Suborder Number, Order Type, Billing Name, Date Received Start and End.
                         Order Number, Suborder Number, and Billing Name are input fields.
                         Order Type is a dropdown listing the types of orders requested
                         Date Received Start and End are input fields that call the React Datepicker component
                         */}

                        <Form.Input label="Order Number"
                                    placeholder="Order Number"
                                    children={
                                        <MaskedInput
                                            mask={[/\d/, /\d/, /\d/, /\d/, /\d/, /\d/, /\d/, /\d/, /\d/, /\d/]}
                                            guide="false"
                                            placeholder="Order Number"/>
                                    }
                        />

                        <Form.Input label="Suborder Number"
                                    placeholder='Suborder Number'
                                    children={
                                        <MaskedInput
                                            mask={[/\d/, /\d/, /\d/, /\d/, /\d/, /\d/, /\d/, /\d/, /\d/, /\d/]}
                                            placeholder="Order Number"/>
                                    }
                        />
                        <Form.Select label="Order Type" defaultValue="all" options={options}/>
                        <Form.Field label="Billing Name" placeholder="Billing Name" control="input"/>
                        <Form.Field onKeyPress={this.handleKeyPress}>
                            <label>Date Received Start</label>
                            <Date />
                        </Form.Field>
                        <Form.Field onKeyPress={this.handleKeyPress}>
                            <label>Date Received End</label>
                            <Date />
                        </Form.Field>
                        <Button type="reset" content="Clear"/>
                        <Button type='submit' positive floated="right" content="Apply"/>
                    </Form>
                </div>
            </Container>
        )
    }
}


export default OrderForm

