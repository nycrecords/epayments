import React from 'react';
import {Button, Grid, Popup, Form} from 'semantic-ui-react';
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
        };

    }

    handleChange = (e) => {
        const target = e.target;
        const value = target.value;
        const name = target.name;
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
                                     onChange={(e, {value}) => {
                                         this.setState({orderType: value});
                                         this.props.callBack("orderType", value, this.props.index, this.props.state.orderType);
                                         //toggles hidden forms for Tax Photo if selected
                                         (this.orderList.indexOf(value) === 0) ?
                                             this.props.callBack("showTaxForm", true, this.props.index, this.props.state.showTaxForm) :
                                             this.props.callBack("showTaxForm", false, this.props.index, this.props.state.showTaxForm);
                                         //toggles hidden forms for Photo Gallery if selected
                                         (this.orderList.indexOf(value) === 1) ?
                                             this.props.callBack("showPhotoGalleryForm", true, this.props.index, this.props.state.showPhotoGalleryForm) :
                                             this.props.callBack("showPhotoGalleryForm", false, this.props.index, this.props.state.showPhotoGalleryForm);
                                         (this.orderList.indexOf(value) === 2) ?
                                             this.props.callBack("showPropertyForm", true, this.props.index, this.props.state.showPropertyForm) :
                                             this.props.callBack("showPropertyForm", false, this.props.index, this.props.state.showPropertyForm);
                                         (this.orderList.indexOf(value) === 3) ?
                                             this.props.callBack("showMarriageSearch", true, this.props.index, this.props.state.showMarriageSearch) :
                                             this.props.callBack("showMarriageSearch", false, this.props.index, this.props.state.showMarriageSearch);
                                         (this.orderList.indexOf(value) === 4) ?
                                             this.props.callBack("showMarriageCert", true, this.props.index, this.props.state.showMarriageCert) :
                                             this.props.callBack("showMarriageCert", false, this.props.index, this.props.state.showMarriageCert);
                                         (this.orderList.indexOf(value) === 5) ?
                                             this.props.callBack("showDeathSearch", true, this.props.index, this.props.state.showDeathSearch) :
                                             this.props.callBack("showDeathSearch", false, this.props.index, this.props.state.showDeathSearch);
                                         (this.orderList.indexOf(value) === 6) ?
                                             this.props.callBack("showDeathCert", true, this.props.index, this.props.state.showDeathCert) :
                                             this.props.callBack("showDeathCert", false, this.props.index, this.props.state.showDeathCert);
                                         (this.orderList.indexOf(value) === 7) ?
                                             this.props.callBack("showBirthSearch", true, this.props.index, this.props.state.showBirthSearch) :
                                             this.props.callBack("showBirthSearch", false, this.props.index, this.props.state.showBirthSearch);
                                         (this.orderList.indexOf(value) === 8) ?
                                             this.props.callBack("showBirthCert", true, this.props.index, this.props.state.showBirthCert) :
                                             this.props.callBack("showBirthCert", false, this.props.index, this.props.state.showBirthCert);
                                     }}
                                     value={this.props.state.orderType[this.props.index]}
                        />

                        {this.props.state.showTaxForm[this.props.index] &&
                        <TaxPhotoForm callBack={this.props.callBack} index={this.props.index}
                                      state={this.props.state}
                                      boroughOptions={boroughOptions}/>}
                        {this.props.state.showPhotoGalleryForm[this.props.index] &&
                        <PhotoGalleryForm callBack={this.props.callBack} index={this.props.index}
                                          state={this.props.state}/>}
                        {this.props.state.showPropertyForm[this.props.index] &&
                        <PropertyCardForm callBack={this.props.callBack} index={this.props.index}
                                          state={this.props.state} boroughOptions={boroughOptions}/>}
                        {this.props.state.showMarriageSearch[this.props.index] &&
                        <MarriageSearchForm callBack={this.props.callBack} index={this.props.index}
                                            state={this.props.state} boroughOptions={boroughOptions}/>}
                        {this.props.state.showMarriageCert[this.props.index] &&
                        <MarriageCertForm callBack={this.props.callBack} index={this.props.index}
                                          state={this.props.state} boroughOptions={boroughOptions}/>}
                        {this.props.state.showDeathSearch[this.props.index] &&
                        <DeathSearchForm callBack={this.props.callBack} index={this.props.index}
                                         state={this.props.state} boroughOptions={boroughOptions}/>}
                        {this.props.state.showDeathCert[this.props.index] &&
                        <DeathCertForm callBack={this.props.callBack} index={this.props.index}
                                       state={this.props.state} boroughOptions={boroughOptions}/>}
                        {this.props.state.showBirthSearch[this.props.index] &&
                        <BirthSearchForm callBack={this.props.callBack} index={this.props.index}
                                         state={this.props.state} genderOptions={genderOptions}
                                         boroughOptions={boroughOptions}/>}
                        {this.props.state.showBirthCert[this.props.index] &&
                        <BirthCertForm callBack={this.props.callBack} index={this.props.index}
                                       state={this.props.state} boroughOptions={boroughOptions}
                                       genderOptions={genderOptions}/>}


                        <Form.Input label="Number of Copies"
                                    name="numCopies"
                                    placeholder="Number of Copies"
                                    required
                                    maxLength={2}
                                    onChange={(e, {value}) => {
                                        if (/^[0-9]+$/.test(value.slice(-1)) || value === '') {
                                            this.setState({numCopies: value});
                                            this.props.callBack("numCopies", value, this.props.index, this.props.state.numCopies);

                                        }
                                    }}
                                    value={this.props.state.numCopies[this.props.index]}
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
                                     value={this.props.state.status[this.props.index]}
                        />
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        );
    }
}

export default SubOrderForm;