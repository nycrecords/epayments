import React from 'react';
import {Button, Form, Grid, Popup, Segment} from 'semantic-ui-react';
import TaxPhotoForm from "./taxPhotoForm"
import PhotoGalleryForm from "./photoGalleryForm"
import {BirthForm} from "./birthForm"
import {MarriageForm} from "./marriageForm";
import {DeathForm} from "./deathForm";


const orderTypeOptions = [
    {key: 'birthcert', text: 'Birth Certificate', value: 'Birth Cert'},
    {key: 'deathcert', text: 'Death Certificate', value: 'Death Cert'},
    {key: 'marriagecert', text: 'Marriage Certificate', value: 'Marriage Cert'},
    {key: 'taxphoto', text: 'Tax Photo', value: 'Tax Photo'},
    {key: 'photogallery', text: 'Photo Gallery', value: 'Photo Gallery'},
];
const statusOptions = [
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

class NewSuborderForm extends React.Component {
    constructor() {
        super();
        this.state = {
            orderType: '',
            numCopies: '1',
            status: '',
        };

        this.handleChange = this.handleChange.bind(this);
    }

    clearSelection = () => {
        this.setState({
            orderType: '',
            numCopies: '1',
            status: '',
        });
    };

    handleChange = (e) => {
        this.setState({
            [e.target.name]: e.target.value
        });
        this.props.handleSuborderListChange(e.target.name, e.target.value, this.props.suborderKey);
    };

    handleFormChange = (name, value) => {
        this.props.handleSuborderListChange(name, value, this.props.suborderKey);
    };

    handleSelectChange = (e, data) => {
        this.setState({
            [data.name]: data.value
        });
        this.props.handleSuborderListChange(data.name, data.value, this.props.suborderKey);
    };

    render() {
        let suborderForm;
        switch (this.state.orderType) {
            case 'Birth Cert':
                suborderForm = (
                    <BirthForm handleFormChange={this.handleFormChange}/>
                );
                break;
            case 'Death Cert':
                suborderForm = (
                    <DeathForm handleFormChange={this.handleFormChange}/>
                );
                break;
            case 'Marriage Cert':
                suborderForm = (
                    <MarriageForm handleFormChange={this.handleFormChange}/>
                );
                break;
            case 'Tax Photo':
                suborderForm = (
                    <TaxPhotoForm handleFormChange={this.handleFormChange}/>
                );
                break;
            case 'Photo Gallery':
                suborderForm = (
                    <PhotoGalleryForm handleFormChange={this.handleFormChange}/>
                );
                break;
            // case 'Property Card':
            //     suborderForm = (
            //         <PropertyCardForm index={this.props.index} />
            //     );
            //     break;
            // no default
        }

        return (
            <Segment color={'black'}>
                <Grid>
                    <Grid.Row>
                        <Grid.Column>
                            <Popup trigger={
                                <Button floated="right" type="button" size="mini" icon='remove' color='red' compact
                                        onClick={() => {
                                            this.clearSelection();
                                            this.props.deleteSuborder(this.props.suborderKey)
                                        }}>
                                </Button>} content={"Remove"}
                            />
                            <h4>
                                Suborder: {this.props.index + 1}
                            </h4>

                            <Form.Select label="Order Type"
                                         required
                                         name="orderType"
                                         placeholder="Order Type"
                                         options={orderTypeOptions}
                                         onChange={this.handleSelectChange}
                                         value={this.state.orderType}
                            />

                            {suborderForm}

                            <Form.Input label="Number of Copies"
                                        name="numCopies"
                                        placeholder="Number of Copies"
                                        required
                                        maxLength={2}
                                        onChange={(e, {value}) => {
                                            if (/^[0-9]+$/.test(value.slice(-1)) || value === '') {
                                                this.handleChange(e)
                                            }
                                        }}
                                        value={this.state.numCopies}
                            />

                            <Form.Select label="Status"
                                         required
                                         name="status"
                                         placeholder="Status"
                                         options={statusOptions}
                                         onChange={this.handleSelectChange}
                                         value={this.state.status}
                            />
                            <br/>
                        </Grid.Column>
                    </Grid.Row>
                </Grid>
            </Segment>
        );
    }
}

export default NewSuborderForm;
