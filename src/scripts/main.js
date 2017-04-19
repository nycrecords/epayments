/* global $ */
// import {browserHistory} from 'react-router'

import React from 'react';
import ReactDOM from 'react-dom';
import {
    Router,
    Route,
    // Link,
    // IndexRoute,
    // hashHistory,
    browserHistory
} from 'react-router';

import App from './components/app.js';
import Header from './components/header.js';
import Inventory from './components/inventory.js';
import Order from './components/order.js';
import OrderForm from './components/orderform.js';

/*
 App
 <App />
 Return the homepage of the ePayments website. The App component includes the Inventory and Order components.
 Inventory -- tagline of 'Department of Records' and filterOrder function is passed
 Order -- state of order object and state of uniqueOrders object is passed

 Functions:
 getInitialState -- initalizes three empty lists named order, uniqueOrders, and orderFilters
 componentDidMount -- accesses orders from the database and updates the objects in the state
 componentWillUnmount -- throws an error if data is not received successfully
 filterOrder -- takes an object order as a parameter and filters orders in the database
 */

// var App = React.createClass({
//     propTypes: {
//         source: React.PropTypes.string.isRequired
//     },
//
//     getInitialState: function () {
//         // Initializes the state with three empty arrays called order, uniqueOrders, and orderFilters
//         return {
//             order: [], // all suborders returned from ajax call
//             uniqueOrders: [], // all unique orders returned from ajax call
//             orderFilters: [] // order filters when 'Apply' button is pressed
//         }
//     },
//     componentDidMount: function () {
//         // initial ajax called on load to set initial states
//         this.serverRequest = $.get(this.props.source, function (result) {
//             for (var i = 0; i < result.orders.length; i++) {
//                 (this.state.order).push(result.orders[i]);
//             }
//             var allUniqueOrders = [];
//             for (i = 0; i < this.state.order.length; i++) {
//                 if (allUniqueOrders.indexOf(this.state.order[i].orderno) === -1) {
//                     allUniqueOrders.push(this.state.order[i].orderno)
//                 }
//             }
//             this.setState({uniqueOrders: allUniqueOrders});
//         }.bind(this))
//     },
//     componentWillUnmount: function () {
//         // performs cleanup of DOM elements created in componentDidMount before a component is unmounted
//         this.serverRequest.abort()
//     },
//     filterOrder: function (order) {
//         // function is called from findOrder() in the OrderForm component
//         // ajax call that passes back a dictionary containing the fields of the order form to retrieve filtered orders
//         this.state.order = [];
//         var dateRangeOrders = [];
//         var allUniqueOrders = [];
//         var orderNumber = order.orderNumber;
//         var subOrderNumber = order.subOrderNumber;
//         var orderType = order.orderType;
//         var billingName = order.billingName;
//         var dateReceivedStart = order.dateReceivedStart;
//         var dateReceivedEnd = order.dateReceivedEnd;
//         if (Date.parse(dateReceivedStart) > Date.parse(dateReceivedEnd)) {
//             alert("Invalid Date Range: 'Date Received - Start' cannot be after 'Date Received - End'.")
//         }
//         this.serverRequest = $.ajax({
//             url: this.props.source,
//             dataType: 'json',
//             type: 'POST',
//             data: {
//                 order_number: orderNumber,
//                 suborder_number: subOrderNumber,
//                 order_type: orderType,
//                 billing_name: billingName,
//                 date_received_start: dateReceivedStart,
//                 date_received_end: dateReceivedEnd
//             },
//             success: function (data) {
//                 for (var i = 0; i < data.orders.length; i++) {
//                     dateRangeOrders.push(data.orders[i])
//                 }
//                 this.setState({order: dateRangeOrders});
//                 for (i = 0; i < this.state.order.length; i++) {
//                     if (allUniqueOrders.indexOf(this.state.order[i].orderno) === -1) {
//                         allUniqueOrders.push(this.state.order[i].orderno)
//                     }
//                 }
//                 this.setState({uniqueOrders: allUniqueOrders});
//             }.bind(this),
//             error: function (xhr, status, err) {
//                 console.error(this.props.url, status, err.toString());
//             }.bind(this)
//         });
//     },
//     render: function () {
//         return (
//             <div className='epayments'>
//                 <Inventory tagline='Department of Records' filterOrder={this.filterOrder}
//                            orderFilters={this.state.orderFilters}/>
//                 <Order order={this.state.order} uniqueOrders={this.state.uniqueOrders}
//                        orderFilters={this.state.orderFilters}/>
//             </div>
//         )
//     }
// });

/*
 Header
 <Header />
 Return the Header component that is used in the Inventory component.
 Uses the tagline passed from the App component into the Inventory component.
 */
// var Header = React.createClass({
//     propTypes: {
//         tagline: React.PropTypes.string.isRequired
//     },
//
//     render: function () {
//         return (
//             <header className='top'>
//                 <h1>ePayments</h1>
//                 <h3 className='tagline'><span>{this.props.tagline}</span></h3>
//             </header>
//         )
//     }
// });


/*
 Inventory
 <Inventory />
 Returns the Inventory component used in the App component.
 Uses the Header and OrderForm components.
 */

// var Inventory = React.createClass({
//     propTypes: {
//         tagline: React.PropTypes.string.isRequired
//     },
//
//     render: function () {
//         return (
//             <div>
//                 <Header tagline={this.props.tagline}/>
//                 <br />
//                 <OrderForm {...this.props} />
//             </div>
//         )
//     }
// });

/*
 Order
 <Order />
 Returns the Order component used in the App component.
 Uses the states of order and uniqueOrders passed from the App component.

 Functions:
 printOrders -- prints each order according to their order type
 printBigLabels -- prints big labels for every order on the page
 printSmallLabels -- prints small labels for every order on the page
 */

// var Order = React.createClass({
//     printOrders: function (event) {
//         // creates a new div for each order that is inserted into the div with id called 'printorders' in index.html
//         // depending on the order type, there will be different HTML formatting
//         for (var i = 0; i < this.props.order.length; i++) {
//             var div = document.createElement('div');
//             div.className = 'separateorder';
//             div.style.fontFamily = 'Arial, Helvetica, sans-serif';
//             div.style.fontSize = '14px';
//             var order = this.props.order[i];
//             var clientsData = order.clientsata.split('|');
//             var address = order.ship_to_streetadd ? order.ship_to_street_add2 == null : order.ship_to_streetadd + ' ' + order.ship_to_street_add2;
//             var orderTypeList = order.ordertypes.split(',');
//             if (orderTypeList.length > 1) {
//                 var orderTypes = <b>This item was ordered with multiple items in Cart: </b>;
//                 if (orderTypeList.indexOf('tax photo') != -1) {
//                     orderTypes += 'Photo Tax, ';
//                 }
//                 if (orderTypeList.indexOf('Property card') != -1) {
//                     orderTypes += 'Property Card, ';
//                 }
//                 if (orderTypeList.indexOf('online gallery') != -1) {
//                     orderTypes += 'Photo Gallery, ';
//                 }
//                 if (orderTypeList.indexOf('Birth search') != -1) {
//                     orderTypes += 'Birth Search, ';
//                 }
//                 if (orderTypeList.indexOf('Birth cert') != -1) {
//                     orderTypes += 'Birth Certificate, ';
//                 }
//                 if (orderTypeList.indexOf('Marriage search') != -1) {
//                     orderTypes += 'Marriage Search, ';
//                 }
//                 if (orderTypeList.indexOf('Marriage cert') != -1) {
//                     orderTypes += 'Marriage Certificate, ';
//                 }
//                 if (orderTypeList.indexOf('Death search') != -1) {
//                     orderTypes += 'Death Search, ';
//                 }
//                 if (orderTypeList.indexOf('Death cert') != -1) {
//                     orderTypes += 'Death Certificate';
//                 }
//                 if (orderTypes.substr(orderTypes.length - 1) == ' ') {
//                     orderTypes = orderTypes.slice(0, -2);
//                 }
//                 orderTypes += '<br>';
//             } else {
//                 orderTypes = '';
//             }
//             if (order.clientagencyname == 'Birth Search') {
//                 var gender = '',
//                     lastName = '',
//                     middleName = '',
//                     firstName = '',
//                     fatherName = '',
//                     motherName = '',
//                     relationship = '',
//                     purpose = '',
//                     additionalCopy = '',
//                     month = '',
//                     day = '',
//                     birthPlace = '',
//                     year = '',
//                     borough = '',
//                     letter = '',
//                     comment = '';
//
//                 if (clientsData.indexOf('GENDER') >= 0) {
//                     gender = <b>GENDER</b> + '<br>' + clientsData[clientsData.indexOf('GENDER') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('LASTNAME') >= 0) {
//                     lastName = '<b>LAST_NAME</b>' + '<br>' + clientsData[clientsData.indexOf('LASTNAME') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('MIDDLENAME') >= 0) {
//                     middleName = '<b>MIDDLE_NAME</b>' + '<br>' + clientsData[clientsData.indexOf('MIDDLENAME') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('FIRSTNAME') >= 0) {
//                     firstName = '<b>FIRST_NAME</b>' + '<br>' + clientsData[clientsData.indexOf('FIRSTNAME') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('FATHER_NAME') >= 0) {
//                     fatherName = '<b>FATHER_NAME</b>' + '<br>' + clientsData[clientsData.indexOf('FATHER_NAME') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('MOTHER_NAME') >= 0) {
//                     motherName = '<b>MOTHER_NAME</b>' + '<br>' + clientsData[clientsData.indexOf('MOTHER_NAME') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('RELATIONSHIP') >= 0) {
//                     relationship = '<b>RELATIONSHIP</b>' + '<br>' + clientsData[clientsData.indexOf('RELATIONSHIP') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('PURPOSE') >= 0) {
//                     purpose = '<b>PURPOSE</b>' + '<br>' + clientsData[clientsData.indexOf('PURPOSE') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('ADDITIONAL_COPY') >= 0) {
//                     additionalCopy = '<b>ADDITIONAL_COPY</b>' + '<br>' + clientsData[clientsData.indexOf('ADDITIONAL_COPY') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('MONTH') >= 0) {
//                     month = '<b>MONTH</b>' + '<br>' + clientsData[clientsData.indexOf('MONTH') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('DAY') >= 0) {
//                     day = '<b>DAY</b>' + '<br>' + clientsData[clientsData.indexOf('DAY') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('BIRTH_PLACE') >= 0) {
//                     birthPlace = '<b>BIRTH_PLACE</b>' + '<br>' + clientsData[clientsData.indexOf('BIRTH_PLACE') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('YEAR_') >= 0) {
//                     year = '<b>YEAR</b>' + '<br>' + clientsData[clientsData.indexOf('YEAR_') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('BOROUGH') >= 0) {
//                     borough = '<b>BOROUGH</b>' + '<br>' + clientsData[clientsData.indexOf('BOROUGH') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('LETTER') >= 0) {
//                     letter = '<b>EXEMPLIFICATION_LETTER</b>' + '<br>' + clientsData[clientsData.indexOf('LETTER') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('ADD_COMMENT') >= 0) {
//                     comment = '<b>COMMENT</b>' + '<br>' + clientsData[clientsData.indexOf('ADD_COMMENT') + 1] + '<br><br>';
//                 }
//                 div.innerHTML = order.ship_to_name + '<br>' +
//                     'Address: ' + address + ' ' + order.ship_to_city + ', ' + (order.ship_to_state == null ? '' : order.ship_to_state) + ' ' + order.ship_to_country + ' ' + order.ship_to_zipcode + '<br>' +
//                     '<h3>Birth Search</h3>' + orderTypes +
//                     '<b>Customer Name: ' + order.billingname + '</b><br>' +
//                     '<b>Order Number: ' + order.orderno + '</b><br>' +
//                     '<b>Time of Order: ' + order.datelastmodified + '</b><br>' +
//                     '<b>Phone: ' + order.ship_to_phone + '</b><br>' +
//                     '<b>Email: ' + order.customeremail + '</b><br>' +
//                     '<b>SubOrderNo: ' + order.suborderno + '</b>' + '<br><br>' +
//                     gender + lastName + middleName + firstName + fatherName + motherName + relationship + purpose +
//                     additionalCopy + month + day + birthPlace + year + borough + letter + comment +
//                     '<div class="pagebreak" style="page-break-after: always;"></div>';
//             }
//             else if (order.clientagencyname == 'Marriage Search') {
//                 var lastNameGroom = '',
//                     firstNameGroom = '',
//                     lastNameBride = '',
//                     firstNameBride = '',
//                     copyReq = '',
//                     marriagePlace = '';
//
//                 if (clientsData.indexOf('LASTNAME_G') >= 0) {
//                     lastNameGroom = '<b>LAST_NAME_GROOM</b>' + '<br>' + clientsData[clientsData.indexOf('LASTNAME_G') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('FIRSTNAME_G') >= 0) {
//                     firstNameGroom = '<b>FIRST_NAME_GROOM</b>' + '<br>' + clientsData[clientsData.indexOf('FIRSTNAME_G') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('LASTNAME_B') >= 0) {
//                     lastNameBride = '<b>LAST_NAME_BRIDE</b>' + '<br>' + clientsData[clientsData.indexOf('LASTNAME_B') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('FIRSTNAME_B') >= 0) {
//                     firstNameBride = '<b>FIRST_NAME_BRIDE</b>' + '<br>' + clientsData[clientsData.indexOf('FIRSTNAME_B') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('RELATIONSHIP') >= 0) {
//                     relationship = '<b>RELATIONSHIP</b>' + '<br>' + clientsData[clientsData.indexOf('RELATIONSHIP') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('PURPOSE') >= 0) {
//                     purpose = '<b>PURPOSE</b>' + '<br>' + clientsData[clientsData.indexOf('PURPOSE') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('COPY_REQ') >= 0) {
//                     copyReq = '<b>COPY_REQ</b>' + '<br>' + clientsData[clientsData.indexOf('COPY_REQ') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('MONTH') >= 0) {
//                     month = '<b>MONTH</b>' + '<br>' + clientsData[clientsData.indexOf('MONTH') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('DAY') >= 0) {
//                     day = '<b>DAY</b>' + '<br>' + clientsData[clientsData.indexOf('DAY') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('YEAR_') >= 0) {
//                     year = '<b>YEAR</b>' + '<br>' + clientsData[clientsData.indexOf('YEAR_') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('MARRIAGE_PLACE') >= 0) {
//                     marriagePlace = '<b>MARRIAGE_PLACE</b>' + '<br>' + clientsData[clientsData.indexOf('MARRIAGE_PLACE') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('BOROUGH') >= 0) {
//                     borough = '<b>BOROUGH</b>' + '<br>' + clientsData[clientsData.indexOf('BOROUGH') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('LETTER') >= 0) {
//                     letter = '<b>EXEMPLIFICATION_LETTER</b>' + '<br>' + clientsData[clientsData.indexOf('LETTER') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('ADD_COMMENT') >= 0) {
//                     comment = '<b>COMMENT</b>' + '<br>' + clientsData[clientsData.indexOf('ADD_COMMENT') + 1] + '<br><br>';
//                 }
//                 div.innerHTML = order.ship_to_name + '<br>' +
//                     'Address: ' + address + ' ' + order.ship_to_city + ', ' + (order.ship_to_state == null ? '' : order.ship_to_state) + ' ' + order.ship_to_country + ' ' + order.ship_to_zipcode + '<br>' +
//                     '<h3>Marriage Search</h3>' + orderTypes +
//                     '<b>Customer Name: ' + order.billingname + '</b><br>' +
//                     '<b>Order Number: ' + order.orderno + '</b><br>' +
//                     '<b>Time of Order: ' + order.datelastmodified + '</b><br>' +
//                     '<b>Phone: ' + order.ship_to_phone + '</b><br>' +
//                     '<b>Email: ' + order.customeremail + '</b><br>' +
//                     '<b>SubOrderNo: ' + order.suborderno + '</b>' + '<br><br>' +
//                     lastNameGroom + firstNameGroom + lastNameBride + firstNameBride + relationship + purpose +
//                     copyReq + month + day + year + marriagePlace + borough + letter + comment +
//                     '<div class="pagebreak" style="page-break-after: always;"></div>';
//             }
//             else if (order.clientagencyname == 'Death Search') {
//                 var cemetery = '',
//                     deathPlace = '',
//                     ageOfDeath = '';
//
//                 if (clientsData.indexOf('LASTNAME') >= 0) {
//                     lastName = '<b>LAST_NAME</b>' + '<br>' + clientsData[clientsData.indexOf('LASTNAME') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('MIDDLENAME') >= 0) {
//                     middleName = <b>MIDDLE_NAME</b> + '<br>' + clientsData[clientsData.indexOf('MIDDLENAME') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('FIRSTNAME') >= 0) {
//                     firstName = '<b>FIRST_NAME</b>' + '<br>' + clientsData[clientsData.indexOf('FIRSTNAME') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('RELATIONSHIP') >= 0) {
//                     relationship = '<b>RELATIONSHIP</b>' + '<br>' + clientsData[clientsData.indexOf('RELATIONSHIP') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('PURPOSE') >= 0) {
//                     purpose = '<b>PURPOSE</b>' + '<br>' + clientsData[clientsData.indexOf('PURPOSE') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('COPY_REQ') >= 0) {
//                     copyReq = '<b>COPY_REQ</b>' + '<br>' + clientsData[clientsData.indexOf('COPY_REQ') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('CEMETERY') >= 0) {
//                     cemetery = '<b>CEMETERY</b>' + '<br>' + clientsData[clientsData.indexOf('CEMETERY') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('MONTH') >= 0) {
//                     month = '<b>MONTH</b>' + '<br>' + clientsData[clientsData.indexOf('MONTH') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('DAY') >= 0) {
//                     day = '<b>DAY</b>' + '<br>' + clientsData[clientsData.indexOf('DAY') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('YEAR_') >= 0) {
//                     year = '<b>YEAR</b>' + '<br>' + clientsData[clientsData.indexOf('YEAR_') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('DEATH_PLACE') >= 0) {
//                     deathPlace = '<b>DEATH_PLACE</b>' + '<br>' + clientsData[clientsData.indexOf('DEATH_PLACE') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('AGEOFDEATH') >= 0) {
//                     ageOfDeath = '<b>AGE_OF_DEATH</b>' + '<br>' + clientsData[clientsData.indexOf('AGEOFDEATH') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('BOROUGH') >= 0) {
//                     borough = '<b>BOROUGH</b>' + '<br>' + clientsData[clientsData.indexOf('BOROUGH') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('LETTER') >= 0) {
//                     letter = '<b>EXEMPLIFICATION_LETTER</b>' + '<br>' + clientsData[clientsData.indexOf('LETTER') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('ADD_COMMENT') >= 0) {
//                     comment = '<b>COMMENT</b>' + '<br>' + clientsData[clientsData.indexOf('ADD_COMMENT') + 1] + '<br><br>';
//                 }
//                 div.innerHTML = order.ship_to_name + '<br>' +
//                     'Address: ' + address + ' ' + order.ship_to_city + ', ' + (order.ship_to_state == null ? '' : order.ship_to_state) + ' ' + order.ship_to_country + ' ' + order.ship_to_zipcode + '<br>' +
//                     '<h3>Death Search</h3>' + orderTypes +
//                     '<b>Customer Name: ' + order.billingname + '</b><br>' +
//                     '<b>Order Number: ' + order.orderno + '</b><br>' +
//                     '<b>Time of Order: ' + order.datelastmodified + '</b><br>' +
//                     '<b>Phone: ' + order.ship_to_phone + '</b><br>' +
//                     '<b>Email: ' + order.customeremail + '</b><br>' +
//                     '<b>SubOrderNo: ' + order.suborderno + '</b>' + '<br><br>' +
//                     lastName + middleName + firstName + relationship + purpose + copyReq + cemetery + month + day +
//                     year + deathPlace + ageOfDeath + borough + letter + comment +
//                     '<div class="pagebreak" style="page-break-after: always;"></div>';
//             }
//             else if (order.clientagencyname == 'Birth Cert') {
//                 var certificateNumber = '';
//
//                 if (clientsData.indexOf('CERTIFICATE_NUMBER') >= 0) {
//                     certificateNumber = '<b>CERTIFICATE_NUMBER</b>' + '<br>' + clientsData[clientsData.indexOf('CERTIFICATE_NUMBER') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('GENDER') >= 0) {
//                     gender = '<b>GENDER</b>' + '<br>' + clientsData[clientsData.indexOf('GENDER') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('LASTNAME') >= 0) {
//                     lastName = '<b>LAST_NAME</b>' + '<br>' + clientsData[clientsData.indexOf('LASTNAME') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('MIDDLENAME') >= 0) {
//                     middleName = '<b>MIDDLE_NAME</b>' + '<br>' + clientsData[clientsData.indexOf('MIDDLENAME') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('FIRSTNAME') >= 0) {
//                     firstName = '<b>FIRST_NAME</b>' + '<br>' + clientsData[clientsData.indexOf('FIRSTNAME') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('FATHER_NAME') >= 0) {
//                     fatherName = '<b>FATHER_NAME</b>' + '<br>' + clientsData[clientsData.indexOf('FATHER_NAME') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('MOTHER_NAME') >= 0) {
//                     motherName = '<b>MOTHER_NAME</b>' + '<br>' + clientsData[clientsData.indexOf('MOTHER_NAME') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('RELATIONSHIP') >= 0) {
//                     relationship = '<b>RELATIONSHIP</b>' + '<br>' + clientsData[clientsData.indexOf('RELATIONSHIP') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('PURPOSE') >= 0) {
//                     purpose = '<b>PURPOSE</b>' + '<br>' + clientsData[clientsData.indexOf('PURPOSE') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('ADDITIONAL_COPY') >= 0) {
//                     additionalCopy = '<b>ADDITIONAL_COPY</b>' + '<br>' + clientsData[clientsData.indexOf('ADDITIONAL_COPY') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('MONTH') >= 0) {
//                     month = '<b>MONTH</b>' + '<br>' + clientsData[clientsData.indexOf('MONTH') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('DAY') >= 0) {
//                     day = '<b>DAY</b>' + '<br>' + clientsData[clientsData.indexOf('DAY') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('YEAR1') >= 0) {
//                     year = '<b>YEAR</b>' + '<br>' + clientsData[clientsData.indexOf('YEAR1') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('BIRTH_PLACE') >= 0) {
//                     birthPlace = '<b>BIRTH_PLACE</b>' + '<br>' + clientsData[clientsData.indexOf('BIRTH_PLACE') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('BOROUGH') >= 0) {
//                     borough = '<b>BOROUGH</b>' + '<br>' + clientsData[clientsData.indexOf('BOROUGH') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('LETTER') >= 0) {
//                     letter = '<b>EXEMPLIFICATION_LETTER</b>' + '<br>' + clientsData[clientsData.indexOf('LETTER') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('ADD_COMMENT') >= 0) {
//                     comment = '<b>COMMENT</b>' + '<br>' + clientsData[clientsData.indexOf('ADD_COMMENT') + 1] + '<br><br>';
//                 }
//                 div.innerHTML = order.ship_to_name + '<br>' +
//                     'Address: ' + address + ' ' + order.ship_to_city + ', ' + (order.ship_to_state == null ? '' : order.ship_to_state) + ' ' + order.ship_to_country + ' ' + order.ship_to_zipcode + '<br>' +
//                     '<h3>Birth Cert</h3>' + orderTypes +
//                     '<b>Customer Name: ' + order.billingname + '</b><br>' +
//                     '<b>Order Number: ' + order.orderno + '</b><br>' +
//                     '<b>Time of Order: ' + order.datelastmodified + '</b><br>' +
//                     '<b>Phone: ' + order.ship_to_phone + '</b><br>' +
//                     '<b>Email: ' + order.customeremail + '</b><br>' +
//                     '<b>SubOrderNo: ' + order.suborderno + '</b>' + '<br><br>' +
//                     certificateNumber + gender + lastName + middleName + firstName + fatherName + motherName +
//                     relationship + purpose + additionalCopy + month + day + year + birthPlace + borough + letter + comment +
//                     '<div class="pagebreak" style="page-break-after: always;"></div>';
//             }
//             else if (order.clientagencyname == 'Death Cert') {
//                 if (clientsData.indexOf('LASTNAME') >= 0) {
//                     lastName = '<b>LAST_NAME</b>' + '<br>' + clientsData[clientsData.indexOf('LASTNAME') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('MIDDLENAME') >= 0) {
//                     middleName = '<b>MIDDLE_NAME</b>' + '<br>' + clientsData[clientsData.indexOf('MIDDLENAME') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('FIRSTNAME') >= 0) {
//                     firstName = '<b>FIRST_NAME</b>' + '<br>' + clientsData[clientsData.indexOf('FIRSTNAME') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('RELATIONSHIP') >= 0) {
//                     relationship = '<b>RELATIONSHIP</b>' + '<br>' + clientsData[clientsData.indexOf('RELATIONSHIP') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('PURPOSE') >= 0) {
//                     purpose = '<b>PURPOSE</b>' + '<br>' + clientsData[clientsData.indexOf('PURPOSE') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('COPY_REQ') >= 0) {
//                     copyReq = '<b>COPY_REQ</b>' + '<br>' + clientsData[clientsData.indexOf('COPY_REQ') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('CEMETERY') >= 0) {
//                     cemetery = '<b>CEMETERY</b>' + '<br>' + clientsData[clientsData.indexOf('CEMETERY') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('MONTH') >= 0) {
//                     month = '<b>MONTH</b>' + '<br>' + clientsData[clientsData.indexOf('MONTH') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('DAY') >= 0) {
//                     day = '<b>DAY</b>' + '<br>' + clientsData[clientsData.indexOf('DAY') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('YEAR') >= 0) {
//                     year = '<b>YEAR</b>' + '<br>' + clientsData[clientsData.indexOf('YEAR') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('DEATH_PLACE') >= 0) {
//                     deathPlace = '<b>DEATH_PLACE</b>' + '<br>' + clientsData[clientsData.indexOf('DEATH_PLACE') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('AGEOFDEATH') >= 0) {
//                     ageOfDeath = '<b>AGE_OF_DEATH</b>' + '<br>' + clientsData[clientsData.indexOf('AGEOFDEATH') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('CERTIFICATE_NUMBER') >= 0) {
//                     certificateNumber = '<b>CERTIFICATE_NUMBER</b>' + '<br>' + clientsData[clientsData.indexOf('CERTIFICATE_NUMBER') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('BOROUGH') >= 0) {
//                     borough = '<b>BOROUGH</b>' + '<br>' + clientsData[clientsData.indexOf('BOROUGH') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('LETTER') >= 0) {
//                     letter = '<b>EXEMPLIFICATION_LETTER</b>' + '<br>' + clientsData[clientsData.indexOf('LETTER') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('ADD_COMMENT') >= 0) {
//                     comment = '<b>COMMENT</b>' + '<br>' + clientsData[clientsData.indexOf('ADD_COMMENT') + 1] + '<br><br>';                }
//                 div.innerHTML = order.ship_to_name + '<br>' +
//                     'Address: ' + address + ' ' + order.ship_to_city + ', ' + (order.ship_to_state == null ? '' : order.ship_to_state) + ' ' + order.ship_to_country + ' ' + order.ship_to_zipcode + '<br>' +
//                     '<h3>Death Cert</h3>' + orderTypes +
//                     '<b>Customer Name: ' + order.billingname + '</b><br>' +
//                     '<b>Order Number: ' + order.orderno + '</b><br>' +
//                     '<b>Time of Order: ' + order.datelastmodified + '</b><br>' +
//                     '<b>Phone: ' + order.ship_to_phone + '</b><br>' +
//                     '<b>Email: ' + order.customeremail + '</b><br>' +
//                     '<b>SubOrderNo: ' + order.suborderno + '</b>' + '<br><br>' +
//                     lastName + middleName + firstName + relationship + purpose + copyReq + cemetery + month + day +
//                     year + deathPlace + ageOfDeath + certificateNumber + borough + letter + comment +
//                     '<div class="pagebreak" style="page-break-after: always;}"></div>';
//             }
//             else if (order.clientagencyname == 'Marriage Cert') {
//                 if (clientsData.indexOf('LASTNAME_G') >= 0) {
//                     lastNameGroom = '<b>LAST_NAME_GROOM</b>' + '<br>' + clientsData[clientsData.indexOf('LASTNAME_G') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('FIRSTNAME_G') >= 0) {
//                     firstNameGroom = '<b>FIRST_NAME_GROOM</b>' + '<br>' + clientsData[clientsData.indexOf('FIRSTNAME_G') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('LASTNAME_B') >= 0) {
//                     lastNameBride = '<b>LAST_NAME_BRIDE</b>' + '<br>' + clientsData[clientsData.indexOf('LASTNAME_B') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('FIRSTNAME_B') >= 0) {
//                     firstNameBride = '<b>FIRST_NAME_BRIDE</b>' + '<br>' + clientsData[clientsData.indexOf('FIRSTNAME_B') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('RELATIONSHIP') >= 0) {
//                     relationship = '<b>RELATIONSHIP</b>' + '<br>' + clientsData[clientsData.indexOf('RELATIONSHIP') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('PURPOSE') >= 0) {
//                     purpose = '<b>PURPOSE</b>' + '<br>' + clientsData[clientsData.indexOf('PURPOSE') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('COPY_REQ') >= 0) {
//                     copyReq = '<b>COPY_REQ</b>' + '<br>' + clientsData[clientsData.indexOf('COPY_REQ') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('MONTH') >= 0) {
//                     month = '<b>MONTH</b>' + '<br>' + clientsData[clientsData.indexOf('MONTH') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('DAY') >= 0) {
//                     day = '<b>DAY</b>' + '<br>' + clientsData[clientsData.indexOf('DAY') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('YEAR') >= 0) {
//                     year = '<b>YEAR</b>' + '<br>' + clientsData[clientsData.indexOf('YEAR') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('MARRIAGE_PLACE') >= 0) {
//                     marriagePlace = '<b>MARRIAGE_PLACE</b>' + '<br>' + clientsData[clientsData.indexOf('MARRIAGE_PLACE') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('CERTIFICATE_NUMBER') >= 0) {
//                     certificateNumber = '<b>CERTIFICATE_NUMBER</b>' + '<br>' + clientsData[clientsData.indexOf('CERTIFICATE_NUMBER') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('BOROUGH') >= 0) {
//                     borough = '<b>BOROUGH</b>' + '<br>' + clientsData[clientsData.indexOf('BOROUGH') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('LETTER') >= 0) {
//                     letter = '<b>EXEMPLIFICATION_LETTER</b>' + '<br>' + clientsData[clientsData.indexOf('LETTER') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('ADD_COMMENT') >= 0) {
//                     comment = '<b>COMMENT</b>' + '<br>' + clientsData[clientsData.indexOf('ADD_COMMENT') + 1] + '<br><br>';
//                 }
//                 div.innerHTML = order.ship_to_name + '<br>' +
//                     'Address: ' + address + ' ' + order.ship_to_city + ', ' + (order.ship_to_state == null ? '' : order.ship_to_state) + ' ' + order.ship_to_country + ' ' + order.ship_to_zipcode + '<br>' +
//                     '<h3>Marriage Cert</h3>' + orderTypes +
//                     '<b>Customer Name: ' + order.billingname + '</b><br>' +
//                     '<b>Order Number: ' + order.orderno + '</b><br>' +
//                     '<b>Time of Order: ' + order.datelastmodified + '</b><br>' +
//                     '<b>Phone: ' + order.ship_to_phone + '</b><br>' +
//                     '<b>Email: ' + order.customeremail + '</b><br>' +
//                     '<b>SubOrderNo: ' + order.suborderno + '</b>' + '<br><br>' +
//                     lastNameGroom + firstNameGroom + lastNameBride + firstNameBride + relationship + purpose +
//                     copyReq + month + day + year + marriagePlace + certificateNumber + borough + letter + comment +
//                     '<div class="pagebreak" style="page-break-after: always;}"></div>';
//             }
//             else if (order.clientagencyname == 'Property Card') {
//                 var block = '',
//                     lot = '',
//                     buildingNumber = '',
//                     street = '',
//                     description = '',
//                     certified = '',
//                     mailPickup = '';
//
//                 if (clientsData.indexOf('BOROUGH') >= 0) {
//                     borough = '<b>BOROUGH</b>' + '<br>' + clientsData[clientsData.indexOf('BOROUGH') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('BLOCK') >= 0) {
//                     block = '<b>BLOCK</b>' + '<br>' + clientsData[clientsData.indexOf('BLOCK') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('LOT') >= 0) {
//                     lot = '<b>LOT</b>' + '<br>' + clientsData[clientsData.indexOf('LOT') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('STREET_NUMBER') >= 0) {
//                     buildingNumber = '<b>BUILDING_NUMBER</b>' + '<br>' + clientsData[clientsData.indexOf('STREET_NUMBER') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('STREET') >= 0) {
//                     street = '<b>STREET</b>' + '<br>' + clientsData[clientsData.indexOf('STREET') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('DESCRIPTION') >= 0) {
//                     description = '<b>DESCRIPTION</b>' + '<br>' + clientsData[clientsData.indexOf('DESCRIPTION') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('COPY_OPTIONS') >= 0) {
//                     certified = '<b>CERTIFIED</b>' + '<br>' + clientsData[clientsData.indexOf('COPY_OPTIONS') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('MAIL_PICKUP') >= 0) {
//                     mailPickup = '<b>MAIL_PICKUP</b>' + '<br>' + clientsData[clientsData.indexOf('MAIL_PICKUP') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('ADD_COMMENT') >= 0) {
//                     comment = '<b>COMMENT</b>' + '<br>' + clientsData[clientsData.indexOf('ADD_COMMENT') + 1] + '<br><br>';
//                 }
//                 div.innerHTML = order.ship_to_name + '<br>' +
//                     'Address: ' + address + ' ' + order.ship_to_city + ', ' + (order.ship_to_state == null ? '' : order.ship_to_state) + ' ' + order.ship_to_country + ' ' + order.ship_to_zipcode + '<br>' +
//                     '<h3>Property Card</h3>' + ordertypes +
//                     '<b>Customer Name: ' + order.billingname + '</b><br>' +
//                     '<b>Order Number: ' + order.orderno + '</b><br>' +
//                     '<b>Time of Order: ' + order.datelastmodified + '</b><br>' +
//                     '<b>Phone: ' + order.ship_to_phone + '</b><br>' +
//                     '<b>Email: ' + order.customeremail + '</b><br>' +
//                     '<b>SubOrderNo: ' + order.suborderno + '</b>' + '<br><br>' +
//                     borough + block + lot + buildingNumber + street + description + certified + mailPickup + comment +
//                     '<div class="pagebreak" style="page-break-after: always;}"></div>';
//             }
//             else if (order.clientagencyname == 'Photo Tax') {
//                 var collection = '',
//                     roll = '',
//                     size = '',
//                     contactNumber = '',
//                     copy = '';
//
//                 if (clientsData.indexOf('Collection') >= 0) {
//                     collection = '<b>COLLECTION</b>' + '<br>' + clientsData[clientsData.indexOf('Collection') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('BOROUGH') >= 0) {
//                     borough = '<b>BOROUGH</b>' + '<br>' + clientsData[clientsData.indexOf('BOROUGH') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('ROLL') >= 0) {
//                     roll = '<b>ROLL</b>' + '<br>' + clientsData[clientsData.indexOf('ROLL') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('BLOCK') >= 0) {
//                     block = '<b>BLOCK</b>' + '<br>' + clientsData[clientsData.indexOf('BLOCK') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('LOT') >= 0) {
//                     lot = '<b>LOT</b>' + '<br>' + clientsData[clientsData.indexOf('LOT') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('STREET_NUMBER') >= 0) {
//                     buildingNumber = '<b>BUILDING_NUMBER</b>' + '<br>' + clientsData[clientsData.indexOf('STREET_NUMBER') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('STREET') >= 0) {
//                     street = '<b>STREET</b>' + '<br>' + clientsData[clientsData.indexOf('STREET') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('DESCRIPTION') >= 0) {
//                     description = '<b>DESCRIPTION</b>' + '<br>' + clientsData[clientsData.indexOf('DESCRIPTION') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('TYPE') >= 0) {
//                     size = '<b>SIZE</b>' + '<br>' + clientsData[clientsData.indexOf('TYPE') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('COPIES') >= 0) {
//                     copy = '<b>COPY</b>' + '<br>' + clientsData[clientsData.indexOf('COPIES') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('MAIL_PICKUP') >= 0) {
//                     mailPickup = '<b>MAIL_PICKUP</b>' + '<br>' + clientsData[clientsData.indexOf('MAIL_PICKUP') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('CONTACT_NUMBER') >= 0) {
//                     contactNumber = '<b>CONTACT_NUMBER</b>' + '<br>' + clientsData[clientsData.indexOf('CONTACT_NUMBER') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('ADD_COMMENT') >= 0) {
//                     comment = '<b>COMMENT</b>' + '<br>' + clientsData[clientsData.indexOf('ADD_COMMENT') + 1] + '<br><br>';
//                 }
//                 div.innerHTML = order.ship_to_name + '<br>' +
//                     'Address: ' + address + ' ' + order.ship_to_city + ', ' + (order.ship_to_state == null ? '' : order.ship_to_state) + ' ' + order.ship_to_country + ' ' + order.ship_to_zipcode + '<br>' +
//                     '<h3>Photo Tax</h3>' + orderTypes +
//                     '<b>Customer Name: ' + order.billingname + '</b><br>' +
//                     '<b>Order Number: ' + order.orderno + '</b><br>' +
//                     '<b>Time of Order: ' + order.datelastmodified + '</b><br>' +
//                     '<b>Phone: ' + order.ship_to_phone + '</b><br>' +
//                     '<b>Email: ' + order.customeremail + '</b><br>' +
//                     '<b>SubOrderNo: ' + order.suborderno + '</b>' + '<br><br>' +
//                     collection + borough + roll + block + lot + buildingNumber + street + description + size + copy + mailPickup + contactNumber + comment +
//                     '<div class="pagebreak" style="page-break-after: always;}"></div>';
//             }
//             else if (order.clientagencyname == 'Photo Gallery') {
//                 var imageIdentifier = '',
//                     additional_description = '',
//                     personal_use_agreement = '';
//                 if (clientsData.indexOf('IMAGE_IDENTIFIER') >= 0) {
//                     imageIdentifier = '<b>IMAGE ID/IDENTIFIER</b>' + '<br>' + clientsData[clientsData.indexOf('IMAGE_IDENTIFIER') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('IMAGE_DESCRIPTION') >= 0) {
//                     description = '<b>DESCRIPTION</b>' + '<br>' + clientsData[clientsData.indexOf('IMAGE_DESCRIPTION') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('ADDITIONAL_DESCRIPTION') >= 0) {
//                     additional_description = '<b>ADDITIONAL_DESCRIPTION</b>' + '<br>' + clientsData[clientsData.indexOf('ADDITIONAL_DESCRIPTION') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('SIZE') >= 0) {
//                     size = '<b>SIZE</b>' + '<br>' + clientsData[clientsData.indexOf('SIZE') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('COPIES') >= 0) {
//                     copy = '<b>COPY</b>' + '<br>' + clientsData[clientsData.indexOf('COPIES') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('MAIL_PICKUP') >= 0) {
//                     mailPickup = '<b>MAIL_PICKUP</b>' + '<br>' + clientsData[clientsData.indexOf('MAIL_PICKUP') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('CONTACT_NUMBER') >= 0) {
//                     contactNumber = '<b>CONTACT_NUMBER</b>' + '<br>' + clientsData[clientsData.indexOf('CONTACT_NUMBER') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('PERSONAL_USE_AGREEMENT') >= 0) {
//                     personal_use_agreement = '<b>PERSONAL_USE_AGREEMENT</b>' + '<br>' + clientsData[clientsData.indexOf('PERSONAL_USE_AGREEMENT') + 1] + '<br><br>';
//                 }
//                 if (clientsData.indexOf('ADD_COMMENT') >= 0) {
//                     comment = '<b>COMMENT</b>' + '<br>' + clientsData[clientsData.indexOf('ADD_COMMENT') + 1] + '<br><br>';
//                 }
//                 div.innerHTML = order.ship_to_name + '<br>' +
//                     'Address: ' + address + ' ' + order.ship_to_city + ', ' + (order.ship_to_state == null ? '' : order.ship_to_state) + ' ' + order.ship_to_country + ' ' + order.ship_to_zipcode + '<br>' +
//                     '<h3>Photo Gallery</h3>' + orderTypes +
//                     '<b>Customer Name: ' + order.billingname + '</b><br>' +
//                     '<b>Order Number: ' + order.orderno + '</b><br>' +
//                     '<b>Time of Order: ' + order.datelastmodified + '</b><br>' +
//                     '<b>Phone: ' + order.ship_to_phone + '</b><br>' +
//                     '<b>Email: ' + order.customeremail + '</b><br>' +
//                     '<b>SubOrderNo: ' + order.suborderno + '</b>' + '<br><br>' +
//                     imageIdentifier + description + additional_description + size + copy + mailPickup + contactNumber + personal_use_agreement + comment +
//                     '<div class="pagebreak" style="page-break-after: always;}"></div>';
//             }
//             document.getElementById('printorders').appendChild(div);
//         }
//         var orderpage = window.open();
//         orderpage.document.write(document.getElementById('printorders').innerHTML);
//         orderpage.print();
//         orderpage.close();
//         document.getElementById('printorders').innerHTML = "";
//     },
//     printBigLabels: function (event) {
//         // create a new div for each order that is inserted into the div with id called 'printbiglabels' in index.html
//         for (var i = 0; i < this.props.order.length; i++) {
//             var div = document.createElement('div');
//             div.id = 'biglabel';
//             div.style.width = '50%';
//             div.style.height = '20%';
//             div.style.display = 'inline-block';
//             div.style.fontFamily = 'Arial, Helvetica, sans-serif';
//             div.style.fontSize = '14px';
//             var order = this.props.order[i];
//             var clientsData = order.clientsData.split('|');
//             var photo_address = '';
//
//             if (clientsData.indexOf('CONTACT_NUMBER') >= 0) {
//                 var contactNumber = '<b>CONTACT_NUMBER</b>' + '<br>' +
//                     clientsData[clientsData.indexOf('CONTACT_NUMBER') + 1] + '<br><br>';
//             } else {
//                 contactNumber = '';
//             }
//             if (order.ship_to_street_add_2 == null) {
//                 var address = order.ship_to_streetadd;
//             } else {
//                 address = order.ship_to_streetadd + ' ' + order.ship_to_street_add2;
//             }
//             if (order.clientagencyname == ('Photo Tax' || 'Photo Gallery')) {
//                 photo_address = 'NYC DEPARTMENT OF RECORDS/MUNICIPAL ARCHIVES' + '<br>' + '31 Chambers Street' +
//                     '<br>' + 'New York, NY 10007' + '<br><br>' + '<hr style="width: 95%">' + '<br>';
//             } else {
//                 photo_address = '';
//             }
//
//             if (order.ship_to_name.length > 1) {
//                 div.innerHTML = '<div style="display: table-cell; vertical-align: middle; text-align: center; width: 375px; height: 200px; margin: auto; position: relative;">' +
//                     photo_address + '<b>TO: </b>' + order.ship_to_name + '<br>' + address + '<br>' + order.ship_to_city +
//                     ', ' + (order.ship_to_state == null ? '' : (order.ship_to_state + ' ')) + order.ship_to_country + ' ' + order.ship_to_zipcode + '<br></div>';
//             } else {
//                 div.innerHTML = '<div style="display: table-cell; vertical-align: middle; text-align: center; width: 375px; height: 200px; margin: auto; position: relative;">' +
//                     'CALL FOR PICKUP' + '<br>' + order.billingname + '<br>' + contactNumber + '<br></div>';
//             }
//             document.getElementById('printbiglabels').appendChild(div);
//         }
//         var biglabelpage = window.open();
//         biglabelpage.document.write(document.getElementById('printbiglabels').innerHTML);
//         biglabelpage.print();
//         biglabelpage.close();
//         document.getElementById('printbiglabels').innerHTML = "";
//     },
//     printSmallLabels: function (event) {
//         // create a new div for each order that is inserted into the div with id called 'printsmalllabels' in index.html
//         for (var i = 0; i < this.props.order.length; i++) {
//             var div = document.createElement('div');
//             div.id = 'smalllabel';
//             div.style.width = '33.33%';
//             div.style.height = '10%';
//             div.style.display = 'inline-block';
//             div.style.fontFamily = 'Arial, Helvetica, sans-serif';
//             div.style.fontSize = '14px';
//             var order = this.props.order[i];
//             if (order.ship_to_street_add_2 == null) {
//                 var address = order.ship_to_streetadd;
//             } else {
//                  address = order.ship_to_streetadd + ' ' + order.ship_to_street_add2;
//             }
//             div.innerHTML = '<div style="display: table-cell; text-align: center; width: 210px; height: 100px; padding: 10px 20px 0px; position: relative; outline: solid;">' +
//                 order.ship_to_name + '<br>' + address + '<br>' + order.ship_to_city + ', ' + (order.ship_to_state == null ? '' : order.ship_to_state + ' ') + order.ship_to_country + ' ' +
//                 order.ship_to_zipcode + '<br></div>';
//             document.getElementById('printsmalllabels').appendChild(div);
//         }
//         var smalllabelpage = window.open();
//         smalllabelpage.document.write(document.getElementById('printsmalllabels').innerHTML);
//         smalllabelpage.print();
//         smalllabelpage.close();
//         document.getElementById('printsmalllabels').innerHTML = "";
//     },
//     render: function () {
//         return (
//             <div className='order-wrap'>
//                 <h2 className='order-title'>Orders</h2>
//                 <ul className='order'>
//                     <li className='total'>
//                         <strong>Number of Items:</strong>
//                         {this.props.order.length}
//                         <strong>Number of Orders:</strong>
//                         {this.props.uniqueOrders.length}
//                         <input type="submit" name="submit" value="Print" onClick={this.printOrders}/>
//                         <input type="submit" name="submit" value="Big Labels" onClick={this.printBigLabels}/>
//                         <input type="submit" name="submit" value="Small Labels" onClick={this.printSmallLabels}/>
//                     </li>
//                     {this.props.order.map(function (order) {
//                         return <li key={order.suborderno}>
//                             Order #: {order.orderno}<br/>
//                             Suborder #: {order.suborderno}<br/>
//                             Order Type: {order.clientagencyname}<br/>
//                             Billing Name: {order.billingname}<br/>
//                             Date Received: {(order.datereceived).substr(0, 10)}<br/>
//                         </li>
//                     })}
//                 </ul>
//             </div>
//         )
//     }
// });

/*
 OrderForm
 <OrderForm />
 Return the OrderForm component used in the Inventory component.
 OrderForm includes a field for Order Number, Sub Order Number, Order Type, Billing Name, Date Start, and Date End.
 Uses the filterOrder function passed from the App component into the Inventory component.

 Functions:
 setDate -- sets the state of the today variable to today's date
 findOrder -- upon an event (apply button being clicked), an order object is created using information from the
 OrderForm and passed into the filterOrder function.
 componentWillMount -- calls setDate function on load of the component
 */

// var OrderForm = React.createClass({
//     setDate: function () {
//         // sets the state of the today variable to today's date
//         var today = new Date();
//         var dd = today.getDate();
//         var mm = today.getMonth() + 1;
//         var yyyy = today.getFullYear();
//         if (dd < 10) {
//             dd = '0' + dd
//         }
//         if (mm < 10) {
//             mm = '0' + mm
//         }
//         today = mm + '/' + dd + '/' + yyyy;
//         this.setState({
//             today: today
//         });
//     },
//     findOrder: function (event) {
//         // when 'Apply' button is pressed, an order object is created and passed to the filterOrder(order) function
//         event.preventDefault();
//         debugger;
//         var order = {
//             orderNumber: this.refs.orderNumber.value,
//             subOrderNumber: this.refs.subOrderNumber.value,
//             orderType: this.refs.orderType.value,
//             billingName: this.refs.billingName.value,
//             dateReceivedStart: this.refs.dateReceivedStart.value,
//             dateReceivedEnd: this.refs.dateReceivedEnd.value
//         };
//         this.props.orderFilters.push(order);
//         this.props.filterOrder(order)
//     },
//     componentWillMount: function () {
//         // calls setDate() function on load of component
//         this.setDate();
//     },
//     render: function () {
//         return (
//             <form className='apply-order' ref='orderForm' onSubmit={this.findOrder}>
//                 <input
//                     data-bind='value: orderNumber'
//                     type='text'
//                     ref='orderNumber'
//                     id='order-number'
//                     placeholder='Order Number'/>
//                 <input
//                     data-bind='value: subOrderNumber'
//                     type='text'
//                     ref='subOrderNumber'
//                     id='suborder-number'
//                     placeholder='Suborder Number'/>
//                 <select data-bind='value: orderType' ref='orderType' id='ordertype' defaultValue='Order Type'>
//                     <option disabled>
//                         Order Type
//                     </option>
//                     <option value='All'>
//                         All
//                     </option>
//                     <option value='vitalrecords'>
//                         --Vital Records--
//                     </option>
//                     <option value='Birth Search'>
//                         Birth Search
//                     </option>
//                     <option value='Marriage Search'>
//                         Marriage Search
//                     </option>
//                     <option value='Death Search'>
//                         Death Search
//                     </option>
//                     <option value='Birth Cert'>
//                         Birth Certificate
//                     </option>
//                     <option value='Marriage Cert'>
//                         Marriage Certificate
//                     </option>
//                     <option value='Death Cert'>
//                         Death Certificate
//                     </option>
//                     <option value='photos'>
//                         --Photos--
//                     </option>
//                     <option value='Property Card'>
//                         Property Card
//                     </option>
//                     <option value='Photo Tax'>
//                         Photo Tax
//                     </option>
//                     <option value='Photo Gallery'>
//                         Photo Gallery
//                     </option>
//                     <option disabled value='other'>
//                         --Other--
//                     </option>
//                     <option value='multipleitems'>
//                         Multiple Items In Cart
//                     </option>
//                     <option value='vitalrecordsphotos'>
//                         Vital Records and Photos In Cart
//                     </option>
//                 </select>
//                 <input
//                     data-bind='value: billingName'
//                     type='text'
//                     ref='billingName'
//                     id='billingname'
//                     placeholder='Billing Name'/>
//                 <input
//                     data-bind='value: dateReceivedStart'
//                     type='text'
//                     ref='dateReceivedStart'
//                     placeholder='Date Received - Start'
//                     id='date-received-start'
//                     defaultValue={this.state.today}/>
//                 <input
//                     data-bind='value: dateReceivedEnd'
//                     type='text'
//                     ref='dateReceivedEnd'
//                     placeholder='Date Received - End'
//                     id='date-received-end'/>
//                 <button type='reset'>
//                     Clear
//                 </button>
//                 <button data-bind='click: findOrder' type='submit' name='submit' value='FindOrder'>
//                     Apply
//                 </button>
//                 <br/>
//             </form>
//         )
//     }
// });


ReactDOM.render(
    <div>
        <App source='/api/v1.0/orders'/>,
        <Header />,
        <Inventory />,
        <Order />,
        <OrderForm />
    </div>,
    document.getElementById('main')
);