import React from 'react';
import {Button, Container, Divider, Grid, Header, Form, Loader, Dimmer, FormCheckbox} from 'semantic-ui-react';

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
            certified: ' ',
            orderType: ' ',
            deathPlace: ' ',
            cemetery: ' ',
            gender: ' ',
            fatherName: ' ',
            motherName: ' ',
            birthPlace: ' ',
            lastName: ' ',
            firstName: ' ',
            middleName: ' ',
            certificateNum: ' ',
            groomLastName: ' ',
            groomFirstName: ' ',
            brideLastName: ' ',
            brideFirstName: ' ',
            month: ' ',
            day: ' ',
            year: ' ',
            marriagePlace: ' ',
            letter: false,
            block: ' ',
            lot: ' ',
            row: ' ',
            borough: ' ',
            buildingNum: ' ',
            street: ' ',
            mail: false,
            contactNum: ' ',
            imgId: ' ',
            imgTitle: ' ',
            comment: ' ',
            personalUseAgreement: false,
            addDescription: ' ',
            collection: ' ',
            printSize: ' ',
            numCopies: ' ',
            status: [],
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

    }

    handleChange = (e) => {
        const target = e.target;
        const value = target.value;
        const name = target.name;
        // console.log("name is :"+ name);
        // console.log("value is :"+ value);c
        console.log(this.props.state + "." + name);
        this.props.callBack(name, value, this.props.index, this.props.state + "." + name);

        this.setState({
            [name]: value
        });
    };


    render() {
        const VitalRecordForm = () => (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Group>
                            <Form.Input label="Month"
                                        name="month"
                                        placeholder="Month"
                                        onChange={(e, {value}) => {
                                            this.setState({month: value})
                                            this.props.callBack("month", value, this.props.index, this.props.state.month)
                                        }}
                                        value={this.state.month}
                            />
                            <Form.Input label="Day"
                                        name="day"
                                        maxLength={2}
                                        placeholder="Day"
                                        onChange={(e, {value}) => {
                                            this.setState({day: value})
                                            this.props.callBack("day", value, this.props.index, this.props.state.day)
                                        }}
                                        value={this.state.day}
                            />
                            <Form.Input label="Year"
                                        name="year"
                                        maxLength={4}
                                        placeholder="Year"
                                        onChange={(e, {value}) => {
                                            this.setState({year: value})
                                            this.props.callBack("year", value, this.props.index, this.props.state.year)
                                        }}
                                        value={this.state.year}
                            />
                        </Form.Group>

                        <Form.Select label="Borough"
                                     name="borough"
                                     options={boroughOptions}
                                     placeholder="Borough"
                                     onChange={(e, {value}) => {
                                         this.setState({borough: value});
                                         this.props.callBack("borough", value, this.props.index, this.props.state.borough);

                                     }}
                                     value={this.state.borough}
                        />
                        <Form.Checkbox label="Letter"
                                       name="letter"
                                       onChange={() => {
                                           (this.state.letter === false) ?
                                               this.props.callBack("letter", true, this.props.index, this.props.state.letter) :
                                               this.props.callBack("letter", false, this.props.index, this.props.state.letter);
                                           (this.state.letter === false) ?
                                               this.setState({letter:true}) :
                                               this.setState({letter:false});
                                       }}
                            // checked={this.state.letter === true}
                        />
                        <Form.Input label="Comment"
                                    name="comment"
                                    placeholder="Comment"
                                    onChange={(e, {value}) => {
                                        this.setState({comment: value})
                                        this.props.callBack("comment", value, this.props.index, this.props.state.comment)
                                    }}
                                    value={this.state.comment}
                        />

                    </Grid.Column>
                </Grid.Row>
            </Grid>
        );
        const TaxPhotoForm = () => (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Group inline>
                            <label>Collection</label>
                            <Form.Radio
                                name="collection"
                                label='1940s'
                                checked={this.state.collection === "1940s"}
                                onChange={(e) => {
                                    this.setState({collection: "1940s"})
                                    this.props.callBack("collection", "1940s", this.props.index, this.props.state.collection)
                                }}

                            />
                            <Form.Radio
                                name="collection"
                                label='1980s'
                                checked={this.state.collection === "1980s"}
                                onChange={(e) => {
                                    this.setState({collection: "1980s"})
                                    this.props.callBack("collection", "1980s", this.props.index, this.props.state.collection)
                                }}
                            />
                            <Form.Radio
                                name="collection"
                                label='Both'
                                checked={this.state.collection === "Both"}
                                onChange={(e) => {
                                    this.setState({collection: "Both"})
                                    this.props.callBack("collection", "Both", this.props.index, this.props.state.collection)
                                }}
                            />
                        </Form.Group>

                        <Form.Input label="Block"
                                    name="block"
                                    placeholder="Block"
                                    onChange={(e, {value}) => {
                                        this.setState({block: value})
                                        this.props.callBack("block", value, this.props.index, this.props.state.block)
                                    }}
                                    value={this.state.block}
                        />
                        <Form.Input label="Lot"
                                    name="lot"
                                    placeholder="Lot"
                                    onChange={(e, {value}) => {
                                        this.setState({lot: value})
                                        this.props.callBack("lot", value, this.props.index, this.props.state.lot)
                                    }}
                                    value={this.state.lot}
                        />
                        <Form.Input label="Roll"
                                    name="roll"
                                    placeholder="Roll#"
                                    onChange={(e, {value}) => {
                                        this.setState({roll: e.target.value})
                                        this.props.callBack("roll", value, this.props.index, this.props.state.roll)
                                    }}
                                    value={this.state.roll}
                        />
                        <Form.Group inline>
                            <label>Printing Size</label>

                            <Form.Radio
                                name={"printSize"}
                                label='8" x 10" Print'
                                checked={this.state.printSize === '8x10'}
                                onChange={(e) => {
                                    this.setState({printSize: '8x10'})
                                    this.props.callBack("printSize", '8x10', this.props.index, this.props.state.printSize);
                                }}
                            />

                            <Form.Radio
                                name={"printSize"}
                                label='11" x 14" Print'
                                checked={this.state.printSize === '11x14'}
                                onChange={(e) => {
                                    this.setState({printSize: '11x14'})
                                    this.props.callBack("printSize", '11x14', this.props.index, this.props.state.printSize);
                                }}
                            />
                        </Form.Group>
                        <Form.Select label="Borough"
                                     name="borough"
                                     options={boroughOptions}
                                     placeholder="Borough"
                                     onChange={(e, {value}) => {
                                         this.setState({borough: value});
                                         this.props.callBack("borough", value, this.props.index, this.props.state.borough);

                                     }}
                                     value={this.state.value}
                        />
                        <Form.Input label="Building Number"
                                    name="buildingNum"
                                    placeholder="Building Number"
                                    onChange={(e, {value}) => {
                                        this.setState({buildingNum: value})
                                        this.props.callBack("buildingNum", value, this.props.index, this.props.state.buildingNum)
                                    }}
                                    value={this.state.buildingNum}
                        />
                        <Form.Input label="Street"
                                    name="street"
                                    placeholder="Street"
                                    onChange={(e, {value}) => {
                                        this.setState({street: value})
                                        this.props.callBack("street", value, this.props.index, this.props.state.street)
                                    }}
                                    value={this.state.street}
                        />
                        <Form.Checkbox label="Mail"
                                       name="mail"
                                       onChange={() => {
                                           (this.state.mail === false) ?
                                               this.props.callBack("mail", true, this.props.index, this.props.state.mail):
                                               this.props.callBack("mail", false, this.props.index, this.props.state.mail);
                                           (this.state.mail === false) ?
                                               this.setState({mail: true}) :
                                               this.setState({mail: false})
                                       }}
                        />
                        <Form.Input label="description"
                                    name="addDescription"
                                    placeholder="Description"
                                    onChange={(e, {value}) => {
                                        this.setState({addDescription: value})
                                        this.props.callBack("addDescription", value, this.props.index, this.props.state.addDescription)
                                    }}
                                    value={this.state.addDescription}
                        />
                        <Form.Input label="Contact Number"
                                    name="contactNum"
                                    placeholder="Contact Number"
                                    onChange={(e, {value}) => {
                                        this.setState({contactNum: value})
                                        this.props.callBack("contactNum", value, this.props.index, this.props.state.contactNum)
                                    }}
                                    value={this.state.contactNum}
                        />
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        );
        const PropertyCardForm = () => (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Input label="Block"
                                    name="block"
                                    placeholder="Block"
                                    onChange={(e, {value}) => {
                                        this.setState({block: value})
                                        this.props.callBack("block", value, this.props.index, this.props.state.block)
                                    }}
                                    value={this.state.block}
                        />
                        <Form.Input label="Lot"
                                    name="lot"
                                    placeholder="Lot"
                                    onChange={(e, {value}) => {
                                        this.setState({lot: value})
                                        this.props.callBack("lot", value, this.props.index, this.props.state.lot)
                                    }}
                                    value={this.state.lot}
                        />
                        <Form.Select label="Borough"
                                     required
                                     name="borough"
                                     options={boroughOptions}
                                     placeholder="Borough"
                                     onChange={(e, {value}) => {
                                         this.setState({borough: value});
                                         this.props.callBack("borough", value, this.props.index, this.props.state.borough);

                                     }}
                                     value={this.state.value}
                        />
                        <Form.Input label="Building Number"
                                    name="buildingNum"
                                    placeholder="Building Number"
                                    onChange={(e, {value}) => {
                                        this.setState({buildingNum: value})
                                        this.props.callBack("buildingNum", value, this.props.index, this.props.state.buildingNum)
                                    }}
                                    value={this.state.buildingNum}
                        />
                        <Form.Input label="Street"
                                    name="street"
                                    placeholder="Street"
                                    onChange={(e, {value}) => {
                                        this.setState({street: value})
                                        this.props.callBack("street", value, this.props.index, this.props.state.street)
                                    }}
                                    value={this.state.street}
                        />
                        <Form.Checkbox label="Mail"
                                       name="mail"
                                       onChange={() => {
                                           (this.state.mail === false) ?
                                               this.props.callBack("mail", true, this.props.index, this.props.state.mail):
                                               this.props.callBack("mail", false, this.props.index, this.props.state.mail);
                                           (this.state.mail === false) ?
                                               this.setState({mail: true}) :
                                               this.setState({mail: false})
                                       }}
                        />
                        <Form.Input label="description"
                                    name="addDescription"
                                    placeholder="Description"
                                    onChange={(e, {value}) => {
                                        this.setState({addDescription: value})
                                        this.props.callBack("addDescription", value, this.props.index, this.props.state.addDescription)
                                    }}
                                    value={this.state.addDescription}
                        />
                        <Form.Input label="Contact Number"
                                    name="contactNum"
                                    placeholder="Contact Number"
                                    onChange={(e, {value}) => {
                                        this.setState({contactNum: value})
                                        this.props.callBack("contactNum", value, this.props.index, this.props.state.contactNum)
                                    }}
                                    value={this.state.contactNum}
                        />
                        <Form.Input label="Certified"
                                    name="certified"
                                    placeholder="Certified"
                                    onChange={(e, {value}) => {
                                        this.setState({certified: value})
                                        this.props.callBack("certified", value, this.props.index, this.props.state.certified)
                                    }}
                                    value={this.state.certified}
                        />

                    </Grid.Column>
                </Grid.Row>
            </Grid>

        )
        const MarriageSearchForm = () => (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Group>
                            <Form.Input label="Groom First Name"
                                        name="groomFirstName"
                                        placeholder="Groom First Name"
                                        onChange={(e, {value}) => {
                                            this.setState({groomFirstName: value})
                                            this.props.callBack("groomFirstName", value, this.props.index, this.props.state.groomFirstName)
                                        }}
                                        value={this.state.groomFirstName}
                            />
                            <Form.Input label="Groom Last Name"
                                        name="groomLastName"
                                        placeholder="Groom Last Name"
                                        onChange={(e, {value}) => {
                                            this.setState({groomLastName: value})
                                            this.props.callBack("groomLastName", value, this.props.index, this.props.state.groomLastName)
                                        }}
                                        value={this.state.groomLastName}
                            />
                        </Form.Group>
                        <Form.Group>
                            <Form.Input label="Bride First Name"
                                        name="brideFirstName"
                                        placeholder="Bride First Name"
                                        onChange={(e, {value}) => {
                                            this.setState({brideFirstName: value})
                                            this.props.callBack("brideFirstName", value, this.props.index, this.props.state.brideFirstName)
                                        }}
                                        value={this.state.brideFirstName}
                            />
                            <Form.Input label="Bride Last Name"
                                        name="brideLastName"
                                        placeholder="Bride Last Name"
                                        onChange={(e, {value}) => {
                                            this.setState({brideLastName: value})
                                            this.props.callBack("brideLastName", value, this.props.index, this.props.state.brideLastName)
                                        }}
                                        value={this.state.brideLastName}
                            />
                        </Form.Group>
                        <Form.Input label="Marriage Place"
                                    name="marriagePlace"
                                    placeholder="Marriage Place"
                                    onChange={(e, {value}) => {
                                        this.setState({marriagePlace: value})
                                        this.props.callBack("marriagePlace", value, this.props.index, this.props.state.marriagePlace)
                                    }}
                                    value={this.state.marriagePlace}
                        />
                        {VitalRecordForm()}
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
        const MarriageCertForm = () => (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Input label="Certificate Number"
                                    name="certificateNum"
                                    placeholder="Certificiate Number"
                                    onChange={(e, {value}) => {
                                        this.setState({certificateNum: value})
                                        this.props.callBack("certificateNum", value, this.props.index, this.props.state.certificateNum)
                                    }}
                                    value={this.state.certificateNum}
                        />
                        {MarriageSearchForm()}

                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
        const DeathSearchForm = () => (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Group>
                            <Form.Input label="First Name"
                                        name="firstName"
                                        placeholder="First Name"
                                        onChange={(e, {value}) => {
                                            this.setState({firstName: value})
                                            this.props.callBack("firstName", value, this.props.index, this.props.state.firstName)
                                        }}
                                        value={this.state.firstName}
                            />
                            <Form.Input label="Middle Name"
                                        name="middleName"
                                        placeholder="Middle Name"
                                        onChange={(e, {value}) => {
                                            this.setState({middleName: value})
                                            this.props.callBack("middleName", value, this.props.index, this.props.state.middleName)
                                        }}
                                        value={this.state.middleName}
                            />
                            <Form.Input label="Last Name"
                                        name="lastName"
                                        placeholder="Last Name"
                                        onChange={(e, {value}) => {
                                            this.setState({lastName: value})
                                            this.props.callBack("lastName", value, this.props.index, this.props.state.lastName)
                                        }}
                                        value={this.state.lastName}
                            />
                        </Form.Group>
                        <Form.Input label="Cemetery"
                                    name="cemetery"
                                    placeholder="Cemetery"
                                    onChange={(e, {value}) => {
                                        this.setState({cemetery: value})
                                        this.props.callBack("cemetery", value, this.props.index, this.props.state.cemetery)
                                    }}
                                    value={this.state.cemetery}
                        />
                        <Form.Input label="Death Place"
                                    name="deathPlace"
                                    placeholder="Death Place"
                                    onChange={(e, {value}) => {
                                        this.setState({block: value})
                                        this.props.callBack("block", value, this.props.index, this.props.state.block)
                                    }}
                                    value={this.state.deathPlace}
                        />
                        {VitalRecordForm()}
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )

        const DeathCertForm = () => (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Input label="Certificate Number"
                                    name="certificateNum"
                                    placeholder="Certificate Number"
                                    onChange={(e, {value}) => {
                                        this.setState({certificateNum: value})
                                        this.props.callBack("certificateNum", value, this.props.index, this.props.state.certificateNum)
                                    }}
                                    value={this.state.certificateNum}
                        />
                        {DeathSearchForm()}
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
        const BirthSearchForm = () => (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Group>
                            <Form.Input label="First Name"
                                        name="firstName"
                                        placeholder="First Name"
                                        onChange={(e, {value}) => {
                                            this.setState({firstName: value})
                                            this.props.callBack("firstName", value, this.props.index, this.props.state.firstName)
                                        }}
                                        value={this.state.firstName}
                            />
                            <Form.Input label="Middle Name"
                                        name="middleName"
                                        placeholder="Middle Name"
                                        onChange={(e, {value}) => {
                                            this.setState({middleName: value})
                                            this.props.callBack("middleName", value, this.props.index, this.props.state.middleName)
                                        }}
                                        value={this.state.middleName}
                            />
                            <Form.Input label="Last Name"
                                        name="lastName"
                                        placeholder="Last Name"
                                        onChange={(e, {value}) => {
                                            this.setState({lastName: value})
                                            this.props.callBack("lastName", value, this.props.index, this.props.state.lastName)
                                        }}
                                        value={this.state.lastName}
                            />
                        </Form.Group>
                        <Form.Input label="Birth Place"
                                    name="birthPlace"
                                    placeholder="BirthPlace"
                                    onChange={(e, {value}) => {
                                        this.setState({birthPlace: value})
                                        this.props.callBack("birthPlace", value, this.props.index, this.props.state.birthPlace)
                                    }}
                                    value={this.state.birthPlace}
                        />
                        <Form.Select label="Gender"
                                     required
                                     name="gender"
                                     placeholder="Gender"
                                     options={genderOptions}
                                     onChange={(e, {value}) => {
                                         this.setState({gender: value});
                                         this.props.callBack("gender", value, this.props.index, this.props.state.gender);
                                     }}
                                     value={this.state.value}
                        />
                        <Form.Input label="Mother Name"
                                    name="motherName"
                                    placeholder="Mother Name"
                                    onChange={(e, {value}) => {
                                        this.setState({motherName: value})
                                        this.props.callBack("motherName", value, this.props.index, this.props.state.motherName)
                                    }}
                                    value={this.state.motherName}
                        />
                        <Form.Input label="Father Name"
                                    name="fatherName"
                                    placeholder="Father Name"
                                    onChange={(e, {value}) => {
                                        this.setState({fatherName: value})
                                        this.props.callBack("fatherName", value, this.props.index, this.props.state.fatherName)
                                    }}
                                    value={this.state.fatherName}
                        />
                        {VitalRecordForm()}
                    </Grid.Column>
                </Grid.Row>
            </Grid>


        )
        const BirthCertForm = () => (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Input label="Certificate Number"
                                    name="certificateNum"
                                    placeholder="Certificiate Number"
                                    onChange={(e, {value}) => {
                                        this.setState({certificateNum: value})
                                        this.props.callBack("certificateNum", value, this.props.index, this.props.state.certificateNum)
                                    }}
                                    value={this.state.certificateNum}
                        />
                        {BirthSearchForm()}
                    </Grid.Column>
                </Grid.Row>
            </Grid>


        );
        const PhotoGalleryForm = () => (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Input label="Image Identifier"
                                    name="imgId"
                                    placeholder="Image Identifier"
                                    onChange={(e, {value}) => {
                                        this.setState({imgId: value})
                                        this.props.callBack("imgId", value, this.props.index, this.props.state.imgId)
                                    }}
                                    value={this.state.imgId}
                        />

                        <Form.Input label="Title/Description of Image"
                                    name="imgTitle"
                                    placeholder="Title/Description of Image"
                                    onChange={(e, {value}) => {
                                        this.setState({imgTitle: value})
                                        this.props.callBack("imgTitle", value, this.props.index, this.props.state.imgTitle)
                                    }}
                                    value={this.state.imgTitle}
                        />

                        <Form.Input label="Addition Description"
                                    name="addDescription"
                                    placeholder="Addition Description"
                                    onChange={(e, {value}) => {
                                        this.setState({addDescription: value})
                                        this.props.callBack("addDescription", value, this.props.index, this.props.state.addDescription)
                                    }}
                                    value={this.state.addDescription}
                        />
                        <Form.Checkbox label="Mail"
                                       name="mail"
                                       onChange={() => {
                                           (this.state.mail === false) ?
                                               this.props.callBack("mail", true, this.props.index, this.props.state.mail):
                                               this.props.callBack("mail", false, this.props.index, this.props.state.mail);
                                           (this.state.mail === false) ?
                                               this.setState({mail: true}) :
                                               this.setState({mail: false})
                                       }}
                        />
                        <Form.Input label="Contact Number"
                                    name="contactNum"
                                    placeholder="Contact Number"
                                    onChange={(e, {value}) => {
                                        this.setState({contactNum: value})
                                        this.props.callBack("contactNum", value, this.props.index, this.props.state.contactNum)
                                    }}
                                    value={this.state.contactNum}
                        />
                        <Form.Checkbox label="Personal Use Agreement"
                                       name="personalUseAgreement"
                                       onChange={() => {
                                           (this.state.personalUseAgreement === false) ?
                                               this.props.callBack("personalUseAgreement", true, this.props.index, this.props.state.personalUseAgreement):
                                               this.props.callBack("personalUseAgreement", false, this.props.index, this.props.state.personalUseAgreement);
                                           (this.state.personalUseAgreement === false) ?
                                               this.setState({personalUseAgreement: true}) :
                                               this.setState({personalUseAgreement: false})
                                       }}
                        />
                        <Form.Input label="Comment"
                                    name="comment"
                                    placeholder="Comment"
                                    onChange={(e, {value}) => {
                                        this.setState({comment: value})
                                        this.props.callBack("comment", value, this.props.index, this.props.state.comment)
                                    }}
                                    value={this.state.comment}
                        />
                        <Form.Group inline required>
                            <label>Printing Size</label>

                            <Form.Radio
                                name={"printSize"}
                                label='8" x 10" Print'
                                checked={this.state.printSize === '8x10'}
                                onChange={(e) => {
                                    this.setState({printSize: '8x10'})
                                    this.props.callBack("printSize", '8x10', this.props.index, this.props.state.printSize);
                                }}
                            />

                            <Form.Radio
                                name={"printSize"}
                                label='11" x 14" Print'
                                checked={this.state.printSize === '11x14'}
                                onChange={(e) => {
                                    this.setState({printSize: '11x14'})
                                    this.props.callBack("printSize", '11x14', this.props.index, this.props.state.printSize);
                                }}
                            />

                            <Form.Radio
                                name={"printSize"}
                                label='16" x 20" Print'
                                checked={this.state.printSize === '16x20'}
                                onChange={(e) => {
                                    this.setState({printSize: '16x20'})
                                    this.props.callBack("printSize", '16x20', this.props.index, this.props.state.printSize);
                                }}
                            />

                        </Form.Group>
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        );
        return (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Select label="Order Type"
                                     required
                                     name="orderType"
                                     placeholder="Order Type"
                                     options={orderTypeOptions}
                                     onChange={(e, {value}) => {
                                         console.log("value :" + value);
                                         // this.setState({orderType: value});
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
                                     value={this.state.value}
                        />

                        {this.state.showTaxForm && TaxPhotoForm()}
                        {this.state.showPhotoGalleryForm && PhotoGalleryForm()}
                        {this.state.showPropertyForm && PropertyCardForm()}
                        {this.state.showMarriageSearch && MarriageSearchForm()}
                        {this.state.showMarriageCert && MarriageCertForm()}
                        {this.state.showDeathSearch && DeathSearchForm()}
                        {this.state.showDeathCert && DeathCertForm()}
                        {this.state.showBirthSearch && BirthSearchForm()}
                        {this.state.showBirthCert && BirthCertForm()}


                        <Form.Input label="Number of Copies"
                                    name="numCopies"
                                    placeholder="Number of Copies"
                                    maxLength="2"
                                    onChange={(e, {value}) => {
                                        if (/^[0-9]+$/.test(value.slice(-1)) || value === '') {
                                            this.setState({numCopies: value});
                                            this.props.callBack("numCopies", value, this.props.index, this.props.state.numCopies);

                                        }
                                    }}
                                    value={this.state.value}
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
                                     value={this.state.value}
                        />
                    </Grid.Column>
                </Grid.Row>
            </Grid>


        );


    }

}

export default SubOrderForm;