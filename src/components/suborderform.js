import React from 'react';
import {Button, Grid, Popup, Form} from 'semantic-ui-react';
import TaxPhotoForm from "./taxPhotoForm"
import PropertyCardForm from "./propertyCardForm"
import PhotoGalleryForm from "./photoGalleryForm"
import {BirthForm} from "./birthForm"
import {MarriageCertForm, MarriageSearchForm} from "./marriageForm";
import {DeathCertForm, DeathSearchForm} from "./deathForm";


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

class SubOrderForm extends React.Component {
    constructor() {
        super();
        this.state = {
            orderType: '',
            numCopies: '',
            status: '',
        };

        this.orderList = ['Tax Photo', 'Photo Gallery',
            'Property Card', 'Marriage Search',
            'Marriage Cert', 'Death Search',
            'Death Cert', 'Birth Search',
            'Birth Cert'];

        this.handleChange = this.handleChange.bind(this);
        this.clearSelection = () => {
            this.setState({
                orderType: '',
                numCopies: '',
                status: '',
            })
        };
    }

    handleChange = (e) => {
        this.setState({
            [e.target.name]: e.target.value
        });
        this.props.handleSuborderListChange(e.target.name, e.target.value, this.props.index);
    };

    handleFormChange = (name, value) => {
        this.props.handleSuborderListChange(name, value, this.props.index);
    };

    handleSelectChange = (e, data) => {
        this.setState({
            [data.name]: data.value
        });
        this.props.handleSuborderListChange(data.name, data.value, this.props.index);
    };

    render() {
        let test;
        switch (this.state.orderType) {
            case 'Birth Cert':
                test = (
                    <BirthForm index={this.props.index} handleFormChange={this.handleFormChange} />
                );
                break;
            case 'Death Cert':
                test = (
                    <DeathCertForm index={this.props.index} handleFormChange={this.handleFormChange} />
                );
                break;
            case 'Marriage Cert':
                test = (
                    <MarriageCertForm index={this.props.index} handleFormChange={this.handleFormChange} />
                );
                break;
            case 'Tax Photo':
                test = (
                    <TaxPhotoForm index={this.props.index} handleFormChange={this.handleFormChange} />
                );
                break;
            case 'Photo Gallery':
                test = (
                    <PhotoGalleryForm index={this.props.index} handleFormChange={this.handleFormChange} />
                );
                break;
            // case 'Property Card':
            //     test = (
            //         <PropertyCardForm index={this.props.index} />
            //     );
            //     break;
            // no default
        }

        return (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Popup trigger={
                            <Button floated="right" type="button" size="mini" icon='remove' color='red' compact
                                    onClick={() => {
                                        this.props.deleteSuborder(this.props.index)
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

                        {test}

                        {/*{this.props.state.showTaxForm[this.props.index] &&*/}
                        {/*<TaxPhotoForm callBack={this.props.callBack} index={this.props.index}*/}
                        {/*state={this.props.state}*/}
                        {/*boroughOptions={boroughOptions}/>}*/}
                        {/*{this.props.state.showPhotoGalleryForm[this.props.index] &&*/}
                        {/*<PhotoGalleryForm callBack={this.props.callBack} index={this.props.index}*/}
                        {/*state={this.props.state}/>}*/}
                        {/*{this.props.state.showPropertyForm[this.props.index] &&*/}
                        {/*<PropertyCardForm callBack={this.props.callBack} index={this.props.index}*/}
                        {/*state={this.props.state} boroughOptions={boroughOptions}/>}*/}
                        {/*{this.props.state.showMarriageSearch[this.props.index] &&*/}
                        {/*<MarriageSearchForm callBack={this.props.callBack} index={this.props.index}*/}
                        {/*state={this.props.state} boroughOptions={boroughOptions}/>}*/}
                        {/*{this.props.state.showMarriageCert[this.props.index] &&*/}
                        {/*<MarriageCertForm callBack={this.props.callBack} index={this.props.index}*/}
                        {/*state={this.props.state} boroughOptions={boroughOptions}/>}*/}
                        {/*{this.props.state.showDeathSearch[this.props.index] &&*/}
                        {/*<DeathSearchForm callBack={this.props.callBack} index={this.props.index}*/}
                        {/*state={this.props.state} boroughOptions={boroughOptions}/>}*/}
                        {/*{this.props.state.showDeathCert[this.props.index] &&*/}
                        {/*<DeathCertForm callBack={this.props.callBack} index={this.props.index}*/}
                        {/*state={this.props.state} boroughOptions={boroughOptions}/>}*/}
                        {/*{this.props.state.showBirthSearch[this.props.index] &&*/}
                        {/*<BirthSearchForm callBack={this.props.callBack} index={this.props.index}*/}
                        {/*state={this.props.state} genderOptions={genderOptions}*/}
                        {/*boroughOptions={boroughOptions}/>}*/}
                        {/*{this.props.state.showBirthCert[this.props.index] &&*/}
                        {/*<BirthCertForm callBack={this.props.callBack} index={this.props.index}*/}
                        {/*state={this.props.state} boroughOptions={boroughOptions}*/}
                        {/*genderOptions={genderOptions}/>}*/}


                        <Form.Input label="Number of Copies"
                                    name="numCopies"
                                    placeholder="Number of Copies"
                                    maxLength={2}
                                    onChange={(e, {value}) => {
                                        if (/^[0-9]+$/.test(value.slice(-1)) || value === '') {
                                            this.handleChange(e)
                                        }
                                    }}
                            // onChange={(e, {value}) => {
                            //     if (/^[0-9]+$/.test(value.slice(-1)) || value === '') {
                            //         this.setState({numCopies: value});
                            //         this.props.callBack("numCopies", value, this.props.index, this.props.state.numCopies);
                            //         }
                            // }}
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
        );
    }
}

export default SubOrderForm;