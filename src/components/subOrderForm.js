import React from 'react';
import {Form, Button, Container} from 'semantic-ui-react';
import Date from './datepicker'
import 'react-datepicker/dist/react-datepicker.css'
import 'semantic-ui-css/semantic.min.css';
import moment from 'moment';

class SubOrderForm extends React.Component() {
    constructor() {
        super();

        this.state = {
            certified: '',
            orderType: '',
            deathPlace: '',
            cemetery: '',
            gender: '',
            fatherName: '',
            motherName: '',
            birthPlace: '',
            lastName: '',
            firstName: '',
            middleName: '',
            certificateNum: '',
            groomLastName: '',
            groomFirstName: '',
            brideLastName: '',
            brideFirstName: '',
            month: '',
            day: '',
            year: ' ',
            marriagePlace: '',
            letter: false,
            block: '',
            lot: '',
            row: '',
            borough: ' ',
            buildingNum: '',
            street: '',
            mail: false,
            contactNum: '',
            imgId: '',
            imgTitle: '',
            comment: '',
            personalUseAgreement: false,
            addDescription: '',
            collection: '',
            printSize: '',
            numCopies: ' ',
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
    }

    return(

    );
}