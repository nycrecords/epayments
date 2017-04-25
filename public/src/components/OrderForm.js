/**
 * Created by sinsang on 4/25/17.
 */
import React from 'react';
import {Form, Button, Container} from 'semantic-ui-react';
import 'semantic-ui-css/semantic.min.css';

const options=[
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
]

class OrderForm extends React.Component {
    render() {
        return (
            <Container>
                <Form>
                    <Form.Field width={6}>
                        <Form.Input label="Order Number" placeholder='Order Number' maxLength="64"/>
                        <Form.Input label="Suborder Number" placeholder='Suborder Number' maxLength="64"/>
                        <Form.Select label="Order Type" placeholder="Order Type" options={options}/>
                        <Form.Input label="Billing Name" placeholder="Billing Name" maxLength="64"/>
                        <Form.Input label="Date Received Start" placeholder="Date Received - Start"/>
                        <Form.Input label="Date Received End" placeholder="Date Received - End"/>
                    </Form.Field>
                    <Button.Group>
                        <Button type="reset">Cancel</Button>
                        <Button type='submit' positive>Submit</Button>
                    </Button.Group>
                </Form>
            </Container>
        )
    }
}


export default OrderForm

