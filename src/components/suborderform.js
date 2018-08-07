import React from 'react';
import {Button, Container, Divider, Grid, Popup, Form, Loader, Icon, FormCheckbox} from 'semantic-ui-react';
import TaxPhotoForm from "./taxPhotoForm"
import PropertyCardForm from "./propertyCardForm"
import PhotoGalleryForm from "./photoGalleryForm"
import {BirthSearchForm, BirthCertForm} from "./birthForm"
import {MarriageCertForm, MarriageSearchForm} from "./marriageForm";
import {DeathCertForm, DeathSearchForm} from "./deathForm";

const boroughOptions = [
    {key: 'bronx', text: 'Bronx', value: 'Bronx'},
    {key: 'brooklyn', text: 'Brooklyn', value: 'Brooklyn'},
    {key: 'manhattan', text: 'Manhattan', value: 'Manhattan'},
    {key: 'queens', text: 'Queens', value: 'Queens'},
    {key: 'statenisland', text: 'Staten Island', value: 'Staten Island'},
];

const genderOptions = [
    {key: 'male', text: 'Male', value: 'Male'},
    {key: 'female', text: 'Female', value: 'Female'},
];

const orderTypeOptions = [
    {key: 'birthsearch', text: 'Birth Search', value: 'Birth Search'},
    {key: 'marriagesearch', text: 'Marriage Search', value: 'Marriage Search'},
    {key: 'deathsearch', text: 'Death Search', value: 'Death Search'},
    {key: 'birthcert', text: 'Birth Certificate', value: 'Birth Cert'},
    {key: 'marriagecert', text: 'Marriage Certificate', value: 'Marriage Cert'},
    {key: 'deathcert', text: 'Death Certificate', value: 'Death Cert'},
    {key: 'propertycard', text: 'Property Card', value: 'Property Card'},
    {key: 'taxphoto', text: 'Tax Photo', value: 'Tax Photo'},
    {key: 'photogallery', text: 'Photo Gallery', value: 'Photo Gallery'},
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

class SubOrderForm extends React.Component {
    constructor() {
        super();
        this.state = {
            orderType: '',
            numCopies: '',
            status: '',
            showBirthCert: false,
            showBirthSearch: false,
            showDeathCert: false,
            showDeathSearch: false,
            showMarriageCert: false,
            showMarriageSearch: false,
            showTaxForm: false,
            showPhotoGalleryForm: false,
            showPropertyForm: false,
        }
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
                showBirthCert: false,
                showBirthSearch: false,
                showDeathCert: false,
                showDeathSearch: false,
                showMarriageCert: false,
                showMarriageSearch: false,
                showTaxForm: false,
                showPhotoGalleryForm: false,
                showPropertyForm: false,

            })
        }

    }

    handleChange = (e) => {
        const target = e.target;
        const value = target.value;
        const name = target.name;
        console.log(this.props.state + "." + name);
        this.props.callBack(name, value, this.props.index, this.props.state + "." + name);

        this.setState({
            [name]: value
        });
    };

    render() {
        return (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Popup trigger={
                            <Button floated="right" type="button" size="mini"
                                    onClick={() =>{
                                        this.props.deleteSuborder(this.props.index)
                                    }}>
                                <Icon name="remove"/>
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
                                     onChange={(e, {value}) => {
                                         console.log("value :" + value);
                                         this.setState({orderType: value});
                                         this.props.callBack("orderType", value, this.props.index, this.props.state.orderType);
                                         //toggles hidden forms for Tax Photo if selected
                                         (this.orderList.indexOf(value) === 0) ?
                                             this.setState({showTaxForm: true}) :
                                             this.setState({showTaxForm: false});
                                         //toggles hidden forms for Photo Gallery if selected
                                         (this.orderList.indexOf(value) === 1) ?
                                             this.setState({showPhotoGalleryForm: true}) :
                                             this.setState({showPhotoGalleryForm: false});
                                         (this.orderList.indexOf(value) === 2) ?
                                             this.setState({showPropertyForm: true}) :
                                             this.setState({showPropertyForm: false});
                                         (this.orderList.indexOf(value) === 3) ?
                                             this.setState({showMarriageSearch: true}) :
                                             this.setState({showMarriageSearch: false});
                                         (this.orderList.indexOf(value) === 4) ?
                                             this.setState({showMarriageCert: true}) :
                                             this.setState({showMarriageCert: false});
                                         (this.orderList.indexOf(value) === 5) ?
                                             this.setState({showDeathSearch: true}) :
                                             this.setState({showDeathSearch: false});
                                         (this.orderList.indexOf(value) === 6) ?
                                             this.setState({showDeathCert: true}) :
                                             this.setState({showDeathCert: false});
                                         (this.orderList.indexOf(value) === 7) ?
                                             this.setState({showBirthSearch: true}) :
                                             this.setState({showBirthSearch: false});
                                         (this.orderList.indexOf(value) === 8) ?
                                             this.setState({showBirthCert: true}) :
                                             this.setState({showBirthCert: false});
                                     }}
                                     value={this.state.orderType}
                        />

                        {this.state.showTaxForm && <TaxPhotoForm callBack={this.props.callBack} index={this.props.index}
                                                                 state={this.props.state}
                                                                 boroughOptions={boroughOptions}/>}
                        {this.state.showPhotoGalleryForm &&
                        <PhotoGalleryForm callBack={this.props.callBack} index={this.props.index}
                                          state={this.props.state}/>}
                        {this.state.showPropertyForm &&
                        <PropertyCardForm callBack={this.props.callBack} index={this.props.index}
                                          state={this.props.state} boroughOptions={boroughOptions}/>}
                        {this.state.showMarriageSearch &&
                        <MarriageSearchForm callBack={this.props.callBack} index={this.props.index}
                                            state={this.props.state} boroughOptions={boroughOptions}/>}
                        {this.state.showMarriageCert &&
                        <MarriageCertForm callBack={this.props.callBack} index={this.props.index}
                                          state={this.props.state} boroughOptions={boroughOptions}/>}
                        {this.state.showDeathSearch &&
                        <DeathSearchForm callBack={this.props.callBack} index={this.props.index}
                                         state={this.props.state} boroughOptions={boroughOptions}/>}
                        {this.state.showDeathCert &&
                        <DeathCertForm callBack={this.props.callBack} index={this.props.index}
                                       state={this.props.state} boroughOptions={boroughOptions}/>}
                        {this.state.showBirthSearch &&
                        <BirthSearchForm callBack={this.props.callBack} index={this.props.index}
                                         state={this.props.state} genderOptions={genderOptions}
                                         boroughOptions={boroughOptions}/>}
                        {this.state.showBirthCert &&
                        <BirthCertForm callBack={this.props.callBack} index={this.props.index}
                                       state={this.props.state} boroughOptions={boroughOptions}
                                       genderOptions={genderOptions}/>}


                        <Form.Input label="Number of Copies"
                                    name="numCopies"
                                    placeholder="Number of Copies"
                                    maxLength="2"
                                    onChange={(e, {value}) => {
                                        if (/^[0-9]+$/.test(value.slice(-1)) || value === '') {
                                            console.log("not an alphabet")
                                            this.setState({numCopies: value});
                                            this.props.callBack("numCopies", value, this.props.index, this.props.state.numCopies);

                                        }
                                    }}
                                    value={this.state.numCopies}
                        />

                        <Form.Select label="Status"
                                     required
                                     name="status"
                                     placeholder="Status"
                                     options={statusOptions}
                                     onChange={(e, {value}) => {
                                         this.setState({status: value});
                                         this.props.callBack("status", value, this.props.index, this.props.state.status);
                                     }}
                                     value={this.state.status}
                        />
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        );
    }
}

export default SubOrderForm;