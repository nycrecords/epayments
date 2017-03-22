/* global $ */
import {browserHistory} from 'react-router'

var React = require('react');
var ReactDOM = require('react-dom');

var ReactRouter = require('react-router');
var Router = ReactRouter.Router;
var Route = ReactRouter.Route;

/*
 App
 <App />
 Return the homepage of the ePayments website. The App component includes the Inventory and Order components.
 Inventory -- tagline of 'Department of Records' and filterOrder function is passed
 Order -- state of order object and state of uniqueOrders object is passed

 Functions:
 getInitialState -- initalizes three empty lists named order, prevDayOrders, and uniqueOrders
 componentDidMount -- accesses orders from the database and updates the objects in the state
 componentWillUnmount -- throws an error if data is not received successfully
 filterOrder -- takes an object order as a parameter and filters orders in the database
 */

var App = React.createClass({
    propTypes: {
        source: React.PropTypes.string.isRequired
    },

    getInitialState: function () {
        return {
            order: [],
            prevDayOrders: [],
            uniqueOrders: [],
            orderFilters: []
        }
    },
    componentDidMount: function () {
        this.serverRequest = $.get(this.props.source, function (result) {
            for (var i = 0; i < result.orders.length; i++) {
                (this.state.order).push(result.orders[i]);
            }
            for (var i = 0; i < result.orders.length; i++) {
                (this.state.prevDayOrders).push(result.orders[i])
            }
            var allUniqueOrders = [];
            for (var i = 0; i < this.state.order.length; i++) {
                if (allUniqueOrders.indexOf(this.state.order[i].orderno) === -1) {
                    allUniqueOrders.push(this.state.order[i].orderno)
                }
            }
            this.setState({uniqueOrders: allUniqueOrders});
        }.bind(this))
    },
    componentWillUnmount: function () {
        this.serverRequest.abort()
    },
    filterOrder: function (order) {
        this.state.order = [];
        var dateRangeOrders = [];
        var allUniqueOrders = [];
        var ordernumber = order.ordernumber;
        var subordernumber = order.subordernumber;
        var ordertype = order.ordertype;
        var billingname = order.billingname;
        var datereceivedstart = order.datereceivedstart;
        var datereceivedend = order.datereceivedend;
        if (Date.parse(datereceivedstart) > Date.parse(datereceivedend)) {
            alert("Invalid Date Range: 'Date Received - Start' cannot be after 'Date Received - End'.")
        }
        this.serverRequest = $.ajax({
            url: this.props.source,
            dataType: 'json',
            type: 'POST',
            data: {
                order_number: ordernumber,
                suborder_number: subordernumber,
                order_type: ordertype,
                billing_name: billingname,
                date_received_start: datereceivedstart,
                date_received_end: datereceivedend
            },
            success: function (data) {
                for (var i = 0; i < data.orders.length; i++) {
                    dateRangeOrders.push(data.orders[i])
                }
                this.setState({order: dateRangeOrders});
                for (var i = 0; i < this.state.order.length; i++) {
                    if (allUniqueOrders.indexOf(this.state.order[i].orderno) === -1) {
                        allUniqueOrders.push(this.state.order[i].orderno)
                    }
                }
                this.setState({uniqueOrders: allUniqueOrders});
            }.bind(this),
            error: function (xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    render: function () {
        return (
            <div className='epayments'>
                <Inventory tagline='Department of Records' filterOrder={this.filterOrder}
                           orderFilters={this.state.orderFilters}/>
                <Order order={this.state.order} uniqueOrders={this.state.uniqueOrders}
                       orderFilters={this.state.orderFilters}/>
            </div>
        )
    }
});

/*
 Header
 <Header />
 Return the Header component that is used in the Inventory component.
 Uses the tagline passed from the App component into the Inventory component.
 */

var Header = React.createClass({
    propTypes: {
        tagline: React.PropTypes.string.isRequired
    },

    render: function () {
        return (
            <header className='top'>
                <h1>ePayments</h1>
                <h3 className='tagline'><span>{this.props.tagline}</span></h3>
            </header>
        )
    }
});

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

var OrderForm = React.createClass({
    setDate: function () {
        var today = new Date();
        var dd = today.getDate();
        var mm = today.getMonth() + 1;
        var yyyy = today.getFullYear();
        if (dd < 10) {
            dd = '0' + dd
        }
        if (mm < 10) {
            mm = '0' + mm
        }
        today = mm + '/' + dd + '/' + yyyy;
        this.setState({
            today: today
        });
    },
    findOrder: function (event) {
        event.preventDefault();
        var order = {
            ordernumber: this.refs.ordernumber.value,
            subordernumber: this.refs.subordernumber.value,
            ordertype: this.refs.ordertype.value,
            billingname: this.refs.billingname.value,
            datereceivedstart: this.refs.datereceivedstart.value,
            datereceivedend: this.refs.datereceivedend.value
        };
        this.props.orderFilters.push(order);
        this.props.filterOrder(order)
    },
    componentWillMount: function () {
        this.setDate();
    },
    render: function () {
        return (
            <form className='apply-order' ref='orderForm' onSubmit={this.findOrder}>
                <input
                    data-bind='value: ordernumber'
                    type='text'
                    ref='ordernumber'
                    id='ordernumber'
                    placeholder='Order Number'/>
                <input
                    data-bind='value: subordernumber'
                    type='text'
                    ref='subordernumber'
                    id='subordernumber'
                    placeholder='Suborder Number'/>
                <select data-bind='value: ordertype' ref='ordertype' id='ordertype' defaultValue='Order Type'>
                    <option disabled>
                        Order Type
                    </option>
                    <option value='All'>
                        All
                    </option>
                    <option value='vitalrecords'>
                        --Vital Records--
                    </option>
                    <option value='Birth Search'>
                        Birth Search
                    </option>
                    <option value='Marriage Search'>
                        Marriage Search
                    </option>
                    <option value='Death Search'>
                        Death Search
                    </option>
                    <option value='Birth Cert'>
                        Birth Certificate
                    </option>
                    <option value='Marriage Cert'>
                        Marriage Certificate
                    </option>
                    <option value='Death Cert'>
                        Death Certificate
                    </option>
                    <option value='photos'>
                        --Photos--
                    </option>
                    <option value='Property Card'>
                        Property Card
                    </option>
                    <option value='Photo Tax'>
                        Photo Tax
                    </option>
                    <option value='Photo Gallery'>
                        Photo Gallery
                    </option>
                    <option disabled value='other'>
                        --Other--
                    </option>
                    <option value='multipleitems'>
                        Multiple Items In Cart
                    </option>
                    <option value='vitalrecordsphotos'>
                        Vital Records and Photos In Cart
                    </option>
                </select>
                <input
                    data-bind='value: billingname'
                    type='text'
                    ref='billingname'
                    id='billingname'
                    placeholder='Billing Name'/>
                <input
                    data-bind='value: datereceivedstart'
                    type='text'
                    ref='datereceivedstart'
                    placeholder='Date Received - Start'
                    id='datepicker'
                    defaultValue={this.state.today}/>
                <input
                    data-bind='value: datereceivedend'
                    type='text'
                    ref='datereceivedend'
                    placeholder='Date Received - End'
                    id='datepicker2'/>
                <button type='reset'>
                    Clear
                </button>
                <button data-bind='click: findOrder' type='submit' name='submit' value='FindOrder'>
                    Apply
                </button>
                <br/>
            </form>
        )
    }
});

/*
 Inventory
 <Inventory />
 Returns the Inventory component used in the App component.
 Uses the Header and OrderForm components.
 */

var Inventory = React.createClass({
    propTypes: {
        tagline: React.PropTypes.string.isRequired
    },

    render: function () {
        return (
            <div>
                <Header tagline={this.props.tagline}/>
                <br />
                <OrderForm {...this.props} />
            </div>
        )
    }
});

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

var Order = React.createClass({
    printOrders: function (event) {
        for (var i = 0; i < this.props.order.length; i++) {
            var div = document.createElement('div');
            div.className = 'separateorder';
            div.style.fontFamily = 'Arial, Helvetica, sans-serif';
            div.style.fontSize = '14px';
            var order = this.props.order[i];
            var clientsdata = order.clientsdata.split('|');
            if (order.ship_to_street_add2 == null) {
                var address = order.ship_to_streetadd;
            } else {
                var address = order.ship_to_streetadd + ' ' + order.ship_to_street_add2;
            }
            var ordertypelist = order.ordertypes.split(',');
            if (ordertypelist.length > 1) {
                var ordertypes = '<b>This item was ordered with multiple items in Cart: </b>';
                if (ordertypelist.indexOf('tax photo') != -1) {
                    ordertypes += 'Photo Tax, ';
                }
                if (ordertypelist.indexOf('Property card') != -1) {
                    ordertypes += 'Property Card, ';
                }
                if (ordertypelist.indexOf('online gallery') != -1) {
                    ordertypes += 'Photo Gallery, ';
                }
                if (ordertypelist.indexOf('Birth search') != -1) {
                    ordertypes += 'Birth Search, ';
                }
                if (ordertypelist.indexOf('Birth cert') != -1) {
                    ordertypes += 'Birth Certificate, ';
                }
                if (ordertypelist.indexOf('Marriage search') != -1) {
                    ordertypes += 'Marriage Search, ';
                }
                if (ordertypelist.indexOf('Marriage cert') != -1) {
                    ordertypes += 'Marriage Certificate, ';
                }
                if (ordertypelist.indexOf('Death search') != -1) {
                    ordertypes += 'Death Search, ';
                }
                if (ordertypelist.indexOf('Death cert') != -1) {
                    ordertypes += 'Death Certificate';
                }
                if (ordertypes.substr(ordertypes.length - 1) == ' ') {
                    ordertypes = ordertypes.slice(0, -2);
                }
                ordertypes += '<br>';
            } else {
                ordertypes = '';
            }
            if (order.clientagencyname == 'Birth Search') {
                if (clientsdata.indexOf('LASTNAME') >= 0) {
                    var last_name = '<b>LAST_NAME</b>' + '<br>' + clientsdata[clientsdata.indexOf('LASTNAME') + 1] + '<br><br>';
                } else {
                    var last_name = '<b>LAST_NAME</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('MIDDLENAME') >= 0) {
                    var middle_name = '<b>MIDDLE_NAME</b>' + '<br>' + clientsdata[clientsdata.indexOf('MIDDLENAME') + 1] + '<br><br>';
                } else {
                    var middle_name = '<b>MIDDLE_NAME</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('FIRSTNAME') >= 0) {
                    var first_name = '<b>FIRST_NAME</b>' + '<br>' + clientsdata[clientsdata.indexOf('FIRSTNAME') + 1] + '<br><br>';
                } else {
                    var first_name = '<b>FIRST_NAME</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('RELATIONSHIP') >= 0) {
                    var relationship = '<b>RELATIONSHIP</b>' + '<br>' + clientsdata[clientsdata.indexOf('RELATIONSHIP') + 1] + '<br><br>';
                } else {
                    var relationship = '<b>RELATIONSHIP</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('PURPOSE') >= 0) {
                    var purpose = '<b>PURPOSE</b>' + '<br>' + clientsdata[clientsdata.indexOf('PURPOSE') + 1] + '<br><br>';
                } else {
                    var purpose = '<b>PURPOSE</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('ADDITIONAL_COPY') >= 0) {
                    var additional_copy = '<b>ADDITIONAL_COPY</b>' + '<br>' + clientsdata[clientsdata.indexOf('ADDITIONAL_COPY') + 1] + '<br><br>';
                } else {
                    var additional_copy = '<b>ADDITIONAL_COPY</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('BIRTH_PLACE') >= 0) {
                    var birth_place = '<b>BIRTH_PLACE</b>' + '<br>' + clientsdata[clientsdata.indexOf('BIRTH_PLACE') + 1] + '<br><br>';
                } else {
                    var birth_place = '<b>BIRTH_PLACE</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('YEAR_') >= 0) {
                    var year = '<b>YEAR</b>' + '<br>' + clientsdata[clientsdata.indexOf('YEAR_') + 1] + '<br><br>';
                } else {
                    var year = '<b>YEAR</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('BOROUGH') >= 0) {
                    var borough = '<b>BOROUGH</b>' + '<br>' + clientsdata[clientsdata.indexOf('BOROUGH') + 1] + '<br><br>';
                } else {
                    var borough = '<b>BOROUGH</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                div.innerHTML = order.ship_to_name + '<br>' +
                    'Address: ' + address + ' ' + order.ship_to_city + ', ' + (order.ship_to_state == null ? '' : order.ship_to_state) +  ' ' + order.ship_to_country + ' ' + order.ship_to_zipcode + '<br>' +
                    '<h3>Birth Search</h3>' + ordertypes +
                    '<b>Customer Name: ' + order.billingname + '</b><br>' +
                    '<b>Order Number: ' + order.orderno + '</b><br>' +
                    '<b>Time of Order: ' + order.datelastmodified + '</b><br>' +
                    '<b>Phone: ' + order.ship_to_phone + '</b><br>' +
                    '<b>Email: ' + order.customeremail + '</b><br>' +
                    '<b>SubOrderNo: ' + order.suborderno + '</b>' + '<br><br>' +
                    last_name + middle_name + first_name + relationship + purpose + additional_copy + birth_place + year + borough +
                    '<div class="pagebreak" style="page-break-after: always;"></div>';
            }
            else if (order.clientagencyname == 'Marriage Search') {
                if (clientsdata.indexOf('LASTNAME_G') >= 0) {
                    var last_name_groom = '<b>LAST_NAME_GROOM</b>' + '<br>' + clientsdata[clientsdata.indexOf('LASTNAME_G') + 1] + '<br><br>';
                } else {
                    var last_name_groom = '<b>LAST_NAME_GROOM</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('FIRSTNAME_G') >= 0) {
                    var first_name_groom = '<b>FIRST_NAME_GROOM</b>' + '<br>' + clientsdata[clientsdata.indexOf('FIRSTNAME_G') + 1] + '<br><br>';
                } else {
                    var first_name_groom = '<b>FIRST_NAME_GROOM</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('LASTNAME_B') >= 0) {
                    var last_name_bride = '<b>LAST_NAME_BRIDE</b>' + '<br>' + clientsdata[clientsdata.indexOf('LASTNAME_B') + 1] + '<br><br>';
                } else {
                    var last_name_bride = '<b>LAST_NAME_BRIDE</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('FIRSTNAME_B') >= 0) {
                    var first_name_bride = '<b>FIRST_NAME_BRIDE</b>' + '<br>' + clientsdata[clientsdata.indexOf('FIRSTNAME_B') + 1] + '<br><br>';
                } else {
                    var first_name_bride = '<b>FIRST_NAME_BRIDE</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('RELATIONSHIP') >= 0) {
                    var relationship = '<b>RELATIONSHIP</b>' + '<br>' + clientsdata[clientsdata.indexOf('RELATIONSHIP') + 1] + '<br><br>';
                } else {
                    var relationship = '<b>RELATIONSHIP</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('PURPOSE') >= 0) {
                    var purpose = '<b>PURPOSE</b>' + '<br>' + clientsdata[clientsdata.indexOf('PURPOSE') + 1] + '<br><br>';
                } else {
                    var purpose = '<b>PURPOSE</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('COPY_REQ') >= 0) {
                    var copy_req = '<b>COPY_REQ</b>' + '<br>' + clientsdata[clientsdata.indexOf('COPY_REQ') + 1] + '<br><br>';
                } else {
                    var copy_req = '<b>COPY_REQ</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('MONTH') >= 0) {
                    var month = '<b>MONTH</b>' + '<br>' + clientsdata[clientsdata.indexOf('MONTH') + 1] + '<br><br>';
                } else {
                    var month = '<b>MONTH</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('DAY') >= 0) {
                    var day = '<b>DAY</b>' + '<br>' + clientsdata[clientsdata.indexOf('DAY') + 1] + '<br><br>';
                } else {
                    var day = '<b>DAY</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('YEAR_') >= 0) {
                    var year = '<b>YEAR</b>' + '<br>' + clientsdata[clientsdata.indexOf('YEAR_') + 1] + '<br><br>';
                } else {
                    var year = '<b>YEAR</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('MARRIAGE_PLACE') >= 0) {
                    var marriage_place = '<b>MARRIAGE_PLACE</b>' + '<br>' + clientsdata[clientsdata.indexOf('MARRIAGE_PLACE') + 1] + '<br><br>';
                } else {
                    var marriage_place = '<b>MARRIAGE_PLACE</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('BOROUGH') >= 0) {
                    var borough = '<b>BOROUGH</b>' + '<br>' + clientsdata[clientsdata.indexOf('BOROUGH') + 1] + '<br><br>';
                } else {
                    var borough = '<b>BOROUGH</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                div.innerHTML = order.ship_to_name + '<br>' +
                    'Address: ' + address + ' ' + order.ship_to_city + ', ' + (order.ship_to_state == null ? '' : order.ship_to_state) +  ' ' + order.ship_to_country + ' ' + order.ship_to_zipcode + '<br>' +
                    '<h3>Marriage Search</h3>' + ordertypes +
                    '<b>Customer Name: ' + order.billingname + '</b><br>' +
                    '<b>Order Number: ' + order.orderno + '</b><br>' +
                    '<b>Time of Order: ' + order.datelastmodified + '</b><br>' +
                    '<b>Phone: ' + order.ship_to_phone + '</b><br>' +
                    '<b>Email: ' + order.customeremail + '</b><br>' +
                    '<b>SubOrderNo: ' + order.suborderno + '</b>' + '<br><br>' +
                    last_name_groom + first_name_groom + last_name_bride + first_name_bride + relationship + purpose +
                    copy_req + month + day + year + marriage_place + borough +
                    '<div class="pagebreak" style="page-break-after: always;"></div>';
            }
            else if (order.clientagencyname == 'Death Search') {
                if (clientsdata.indexOf('LASTNAME') >= 0) {
                    var last_name = '<b>LAST_NAME</b>' + '<br>' + clientsdata[clientsdata.indexOf('LASTNAME') + 1] + '<br><br>';
                } else {
                    var last_name = '<b>LAST_NAME</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('MIDDLENAME') >= 0) {
                    var middlename = '<b>MIDDLE_NAME</b>' + '<br>' + clientsdata[clientsdata.indexOf('MIDDLENAME') + 1] + '<br><br>';
                } else {
                    var middlename = '<b>MIDDLE_NAME</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('FIRSTNAME') >= 0) {
                    var first_name = '<b>FIRST_NAME</b>' + '<br>' + clientsdata[clientsdata.indexOf('FIRSTNAME') + 1] + '<br><br>';
                } else {
                    var first_name = '<b>FIRST_NAME</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('RELATIONSHIP') >= 0) {
                    var relationship = '<b>RELATIONSHIP</b>' + '<br>' + clientsdata[clientsdata.indexOf('RELATIONSHIP') + 1] + '<br><br>';
                } else {
                    var relationship = '<b>RELATIONSHIP</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('COPY_REQ') >= 0) {
                    var copy_req = '<b>COPY_REQ</b>' + '<br>' + clientsdata[clientsdata.indexOf('COPY_REQ') + 1] + '<br><br>';
                } else {
                    var copy_req = '<b>COPY_REQ</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('ADD_COMMENT') >= 0) {
                    var add_comment = '<b>ADD_COMMENT</b>' + '<br>' + clientsdata[clientsdata.indexOf('ADD_COMMENT') + 1] + '<br><br>';
                } else {
                    var add_comment = '<b>ADD_COMMENT</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('YEAR_') >= 0) {
                    var year = '<b>YEAR</b>' + '<br>' + clientsdata[clientsdata.indexOf('YEAR_') + 1] + '<br><br>';
                } else {
                    var year = '<b>YEAR</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('BOROUGH') >= 0) {
                    var borough = '<b>BOROUGH</b>' + '<br>' + clientsdata[clientsdata.indexOf('BOROUGH') + 1] + '<br><br>';
                } else {
                    var borough = '<b>BOROUGH</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                div.innerHTML = order.ship_to_name + '<br>' +
                    'Address: ' + address + ' ' + order.ship_to_city + ', ' + (order.ship_to_state == null ? '' : order.ship_to_state) +  ' ' + order.ship_to_country + ' ' + order.ship_to_zipcode + '<br>' +
                    '<h3>Death Search</h3>' + ordertypes +
                    '<b>Customer Name: ' + order.billingname + '</b><br>' +
                    '<b>Order Number: ' + order.orderno + '</b><br>' +
                    '<b>Time of Order: ' + order.datelastmodified + '</b><br>' +
                    '<b>Phone: ' + order.ship_to_phone + '</b><br>' +
                    '<b>Email: ' + order.customeremail + '</b><br>' +
                    '<b>SubOrderNo: ' + order.suborderno + '</b>' + '<br><br>' +
                    last_name + middlename + first_name + relationship + copy_req + add_comment + year + borough +
                    '<div class="pagebreak" style="page-break-after: always;"></div>';
            }
            else if (order.clientagencyname == 'Birth Cert') {
                if (clientsdata.indexOf('CERTIFICATE_NUMBER') >= 0) {
                    var certificate_number = '<b>CERTIFICATE_NUMBER</b>' + '<br>' + clientsdata[clientsdata.indexOf('CERTIFICATE_NUMBER') + 1] + '<br><br>';
                } else {
                    var certificate_number = '<b>CERTIFICATE_NUMBER</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('GENDER') >= 0) {
                    var gender = '<b>GENDER</b>' + '<br>' + clientsdata[clientsdata.indexOf('GENDER') + 1] + '<br><br>';
                } else {
                    var gender = '<b>GENDER</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('LASTNAME') >= 0) {
                    var last_name = '<b>LAST_NAME</b>' + '<br>' + clientsdata[clientsdata.indexOf('LASTNAME') + 1] + '<br><br>';
                } else {
                    var last_name = '<b>LAST_NAME</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('MIDDLENAME') >= 0) {
                    var middle_name = '<b>MIDDLE_NAME</b>' + '<br>' + clientsdata[clientsdata.indexOf('MIDDLENAME') + 1] + '<br><br>';
                } else {
                    var middle_name = '<b>MIDDLE_NAME</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('FIRSTNAME') >= 0) {
                    var first_name = '<b>FIRST_NAME</b>' + '<br>' + clientsdata[clientsdata.indexOf('FIRSTNAME') + 1] + '<br><br>';
                } else {
                    var first_name = '<b>FIRST_NAME</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('FATHER_NAME') >= 0) {
                    var father_name = '<b>FATHER_NAME</b>' + '<br>' + clientsdata[clientsdata.indexOf('FATHER_NAME') + 1] + '<br><br>';
                } else {
                    var father_name = '<b>FATHER_NAME</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('MOTHER_NAME') >= 0) {
                    var mother_name = '<b>MOTHER_NAME</b>' + '<br>' + clientsdata[clientsdata.indexOf('MOTHER_NAME') + 1] + '<br><br>';
                } else {
                    var mother_name = '<b>MOTHER_NAME</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('RELATIONSHIP') >= 0) {
                    var relationship = '<b>RELATIONSHIP</b>' + '<br>' + clientsdata[clientsdata.indexOf('RELATIONSHIP') + 1] + '<br><br>';
                } else {
                    var relationship = '<b>RELATIONSHIP</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('PURPOSE') >= 0) {
                    var purpose = '<b>PURPOSE</b>' + '<br>' + clientsdata[clientsdata.indexOf('PURPOSE') + 1] + '<br><br>';
                } else {
                    var purpose = '<b>PURPOSE</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('ADDITIONAL_COPY') >= 0) {
                    var additional_copy = '<b>ADDITIONAL_COPY</b>' + '<br>' + clientsdata[clientsdata.indexOf('ADDITIONAL_COPY') + 1] + '<br><br>';
                } else {
                    var additional_copy = '<b>ADDITIONAL_COPY</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('MONTH') >= 0) {
                    var month = '<b>MONTH</b>' + '<br>' + clientsdata[clientsdata.indexOf('MONTH') + 1] + '<br><br>';
                } else {
                    var month = '<b>MONTH</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('DAY') >= 0) {
                    var day = '<b>DAY</b>' + '<br>' + clientsdata[clientsdata.indexOf('DAY') + 1] + '<br><br>';
                } else {
                    var day = '<b>DAY</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('YEAR1') >= 0) {
                    var year = '<b>YEAR</b>' + '<br>' + clientsdata[clientsdata.indexOf('YEAR1') + 1] + '<br><br>';
                } else {
                    var year = '<b>YEAR</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('BIRTH_PLACE') >= 0) {
                    var birth_place = '<b>BIRTH_PLACE</b>' + '<br>' + clientsdata[clientsdata.indexOf('BIRTH_PLACE') + 1] + '<br><br>';
                } else {
                    var birth_place = '<b>BIRTH_PLACE</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('BOROUGH') >= 0) {
                    var borough = '<b>BOROUGH</b>' + '<br>' + clientsdata[clientsdata.indexOf('BOROUGH') + 1] + '<br><br>';
                } else {
                    var borough = '<b>BOROUGH</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                div.innerHTML = order.ship_to_name + '<br>' +
                    'Address: ' + address + ' ' + order.ship_to_city + ', ' + (order.ship_to_state == null ? '' : order.ship_to_state) +  ' ' + order.ship_to_country + ' ' + order.ship_to_zipcode + '<br>' +
                    '<h3>Birth Cert</h3>' + ordertypes +
                    '<b>Customer Name: ' + order.billingname + '</b><br>' +
                    '<b>Order Number: ' + order.orderno + '</b><br>' +
                    '<b>Time of Order: ' + order.datelastmodified + '</b><br>' +
                    '<b>Phone: ' + order.ship_to_phone + '</b><br>' +
                    '<b>Email: ' + order.customeremail + '</b><br>' +
                    '<b>SubOrderNo: ' + order.suborderno + '</b>' + '<br><br>' +
                    certificate_number + gender + last_name + middle_name + first_name + father_name + mother_name +
                    relationship + purpose + additional_copy + month + day + year + birth_place + borough +
                    '<div class="pagebreak" style="page-break-after: always;"></div>';
            }
            else if (order.clientagencyname == 'Death Cert') {
                if (clientsdata.indexOf('LASTNAME') >= 0) {
                    var last_name = '<b>LAST_NAME</b>' + '<br>' + clientsdata[clientsdata.indexOf('LASTNAME') + 1] + '<br><br>';
                } else {
                    var last_name = '<b>LAST_NAME</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('MIDDLENAME') >= 0) {
                    var middle_name = '<b>MIDDLE_NAME</b>' + '<br>' + clientsdata[clientsdata.indexOf('MIDDLENAME') + 1] + '<br><br>';
                } else {
                    var middle_name = '<b>MIDDLE_NAME</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('FIRSTNAME') >= 0) {
                    var first_name = '<b>FIRST_NAME</b>' + '<br>' + clientsdata[clientsdata.indexOf('FIRSTNAME') + 1] + '<br><br>';
                } else {
                    var first_name = '<b>FIRST_NAME</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('RELATIONSHIP') >= 0) {
                    var relationship = '<b>RELATIONSHIP</b>' + '<br>' + clientsdata[clientsdata.indexOf('RELATIONSHIP') + 1] + '<br><br>';
                } else {
                    var relationship = '<b>RELATIONSHIP</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('PURPOSE') >= 0) {
                    var purpose = '<b>PURPOSE</b>' + '<br>' + clientsdata[clientsdata.indexOf('PURPOSE') + 1] + '<br><br>';
                } else {
                    var purpose = '<b>PURPOSE</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('COPY_REQ') >= 0) {
                    var copy_req = '<b>COPY_REQ</b>' + '<br>' + clientsdata[clientsdata.indexOf('COPY_REQ') + 1] + '<br><br>';
                } else {
                    var copy_req = '<b>COPY_REQ</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('MONTH') >= 0) {
                    var month = '<b>MONTH</b>' + '<br>' + clientsdata[clientsdata.indexOf('MONTH') + 1] + '<br><br>';
                } else {
                    var month = '<b>MONTH</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('DAY') >= 0) {
                    var day = '<b>DAY</b>' + '<br>' + clientsdata[clientsdata.indexOf('DAY') + 1] + '<br><br>';
                } else {
                    var day = '<b>DAY</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('YEAR') >= 0) {
                    var year = '<b>YEAR</b>' + '<br>' + clientsdata[clientsdata.indexOf('YEAR') + 1] + '<br><br>';
                } else {
                    var year = '<b>YEAR</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('CERTIFICATE_NUMBER') >= 0) {
                    var certificate_number = '<b>CERTIFICATE_NUMBER</b>' + '<br>' + clientsdata[clientsdata.indexOf('CERTIFICATE_NUMBER') + 1] + '<br><br>';
                } else {
                    var certificate_number = '<b>CERTIFICATE_NUMBER</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('BOROUGH') >= 0) {
                    var borough = '<b>BOROUGH</b>' + '<br>' + clientsdata[clientsdata.indexOf('BOROUGH') + 1] + '<br><br>';
                } else {
                    var borough = '<b>BOROUGH</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                div.innerHTML = order.ship_to_name + '<br>' +
                    'Address: ' + address + ' ' + order.ship_to_city + ', ' + (order.ship_to_state == null ? '' : order.ship_to_state) +  ' ' + order.ship_to_country + ' ' + order.ship_to_zipcode + '<br>' +
                    '<h3>Death Cert</h3>' + ordertypes +
                    '<b>Customer Name: ' + order.billingname + '</b><br>' +
                    '<b>Order Number: ' + order.orderno + '</b><br>' +
                    '<b>Time of Order: ' + order.datelastmodified + '</b><br>' +
                    '<b>Phone: ' + order.ship_to_phone + '</b><br>' +
                    '<b>Email: ' + order.customeremail + '</b><br>' +
                    '<b>SubOrderNo: ' + order.suborderno + '</b>' + '<br><br>' +
                    last_name + middle_name + first_name + relationship + purpose + copy_req + month + day + year +
                    certificate_number + borough +
                    '<div class="pagebreak" style="page-break-after: always;}"></div>';
            }
            else if (order.clientagencyname == 'Marriage Cert') {
                if (clientsdata.indexOf('LASTNAME_G') >= 0) {
                    var last_name_groom = '<b>LAST_NAME_GROOM</b>' + '<br>' + clientsdata[clientsdata.indexOf('LASTNAME_G') + 1] + '<br><br>';
                } else {
                    var last_name_groom = '<b>LAST_NAME_GROOM</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('LASTNAME_B') >= 0) {
                    var last_name_bride = '<b>LAST_NAME_BRIDE</b>' + '<br>' + clientsdata[clientsdata.indexOf('LASTNAME_B') + 1] + '<br><br>';
                } else {
                    var last_name_bride = '<b>LAST_NAME_BRIDE</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('COPY_REQ') >= 0) {
                    var copy_req = '<b>COPY_REQ</b>' + '<br>' + clientsdata[clientsdata.indexOf('COPY_REQ') + 1] + '<br><br>';
                } else {
                    var copy_req = '<b>COPY_REQ</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('YEAR') >= 0) {
                    var year = '<b>YEAR</b>' + '<br>' + clientsdata[clientsdata.indexOf('YEAR') + 1] + '<br><br>';
                } else {
                    var year = '<b>YEAR</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('CERTIFICATE_NUMBER') >= 0) {
                    var certificate_number = '<b>CERTIFICATE_NUMBER</b>' + '<br>' + clientsdata[clientsdata.indexOf('CERTIFICATE_NUMBER') + 1] + '<br><br>';
                } else {
                    var certificate_number = '<b>CERTIFICATE_NUMBER</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('BOROUGH') >= 0) {
                    var borough = '<b>BOROUGH</b>' + '<br>' + clientsdata[clientsdata.indexOf('BOROUGH') + 1] + '<br><br>';
                } else {
                    var borough = '<b>BOROUGH</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                div.innerHTML = order.ship_to_name + '<br>' +
                    'Address: ' + address + ' ' + order.ship_to_city + ', ' + (order.ship_to_state == null ? '' : order.ship_to_state) +  ' ' + order.ship_to_country + ' ' + order.ship_to_zipcode + '<br>' +
                    '<h3>Marriage Cert</h3>' + ordertypes +
                    '<b>Customer Name: ' + order.billingname + '</b><br>' +
                    '<b>Order Number: ' + order.orderno + '</b><br>' +
                    '<b>Time of Order: ' + order.datelastmodified + '</b><br>' +
                    '<b>Phone: ' + order.ship_to_phone + '</b><br>' +
                    '<b>Email: ' + order.customeremail + '</b><br>' +
                    '<b>SubOrderNo: ' + order.suborderno + '</b>' + '<br><br>' +
                    last_name_groom + last_name_bride + copy_req + year + certificate_number + borough +
                    '<div class="pagebreak" style="page-break-after: always;}"></div>';
            }
            else if (order.clientagencyname == 'Property Card') {
                if (clientsdata.indexOf('BOROUGH') >= 0) {
                    var borough = '<b>BOROUGH</b>' + '<br>' + clientsdata[clientsdata.indexOf('BOROUGH') + 1] + '<br><br>';
                } else {
                    var borough = '<b>BOROUGH</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('BLOCK') >= 0) {
                    var block = '<b>BLOCK</b>' + '<br>' + clientsdata[clientsdata.indexOf('BLOCK') + 1] + '<br><br>';
                } else {
                    var block = '<b>BLOCK</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('LOT') >= 0) {
                    var lot = '<b>LOT</b>' + '<br>' + clientsdata[clientsdata.indexOf('LOT') + 1] + '<br><br>';
                } else {
                    var lot = '<b>LOT</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('STREET_NUMBER') >= 0) {
                    var building_number = '<b>BUILDING_NUMBER</b>' + '<br>' + clientsdata[clientsdata.indexOf('STREET_NUMBER') + 1] + '<br><br>';
                } else {
                    var building_number = '<b>BUILDING_NUMBER</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('STREET') >= 0) {
                    var street = '<b>STREET</b>' + '<br>' + clientsdata[clientsdata.indexOf('STREET') + 1] + '<br><br>';
                } else {
                    var street = '<b>STREET</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('DESCRIPTION') >= 0) {
                    var description = '<b>DESCRIPTION</b>' + '<br>' + clientsdata[clientsdata.indexOf('DESCRIPTION') + 1] + '<br><br>';
                } else {
                    var description = '<b>DESCRIPTION</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('COPY_OPTIONS') >= 0) {
                    var certified = '<b>CERTIFIED</b>' + '<br>' + clientsdata[clientsdata.indexOf('COPY_OPTIONS') + 1] + '<br><br>';
                } else {
                    var certified = '<b>CERTIFIED</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('MAIL_PICKUP') >= 0) {
                    var mail_pickup = '<b>MAIL_PICKUP</b>' + '<br>' + clientsdata[clientsdata.indexOf('MAIL_PICKUP') + 1] + '<br><br>';
                } else {
                    var mail_pickup = '<b>MAIL_PICKUP</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                div.innerHTML = order.ship_to_name + '<br>' +
                    'Address: ' + address + ' ' + order.ship_to_city + ', ' + (order.ship_to_state == null ? '' : order.ship_to_state) +  ' ' + order.ship_to_country + ' ' + order.ship_to_zipcode + '<br>' +
                    '<h3>Property Card</h3>' + ordertypes +
                    '<b>Customer Name: ' + order.billingname + '</b><br>' +
                    '<b>Order Number: ' + order.orderno + '</b><br>' +
                    '<b>Time of Order: ' + order.datelastmodified + '</b><br>' +
                    '<b>Phone: ' + order.ship_to_phone + '</b><br>' +
                    '<b>Email: ' + order.customeremail + '</b><br>' +
                    '<b>SubOrderNo: ' + order.suborderno + '</b>' + '<br><br>' +
                    borough + block + lot + building_number + street + description + certified + mail_pickup +
                    '<div class="pagebreak" style="page-break-after: always;}"></div>';
            }
            else if (order.clientagencyname == 'Photo Tax') {
                if (clientsdata.indexOf('Collection') >= 0) {
                    var collection = '<b>COLLECTION</b>' + '<br>' + clientsdata[clientsdata.indexOf('Collection') + 1] + '<br><br>';
                } else {
                    var collection = '<b>COLLECTION</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('BOROUGH') >= 0) {
                    var borough = '<b>BOROUGH</b>' + '<br>' + clientsdata[clientsdata.indexOf('BOROUGH') + 1] + '<br><br>';
                } else {
                    var borough = '<b>BOROUGH</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('BLOCK') >= 0) {
                    var block = '<b>BLOCK</b>' + '<br>' + clientsdata[clientsdata.indexOf('BLOCK') + 1] + '<br><br>';
                } else {
                    var block = '<b>BLOCK</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('LOT') >= 0) {
                    var lot = '<b>LOT</b>' + '<br>' + clientsdata[clientsdata.indexOf('LOT') + 1] + '<br><br>';
                } else {
                    var lot = '<b>LOT</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('STREET_NUMBER') >= 0) {
                    var building_number = '<b>BUILDING_NUMBER</b>' + '<br>' + clientsdata[clientsdata.indexOf('STREET_NUMBER') + 1] + '<br><br>';
                } else {
                    var building_number = '<b>BUILDING_NUMBER</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('STREET') >= 0) {
                    var street = '<b>STREET</b>' + '<br>' + clientsdata[clientsdata.indexOf('STREET') + 1] + '<br><br>';
                } else {
                    var street = '<b>STREET</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('DESCRIPTION') >= 0) {
                    var description = '<b>DESCRIPTION</b>' + '<br>' + clientsdata[clientsdata.indexOf('DESCRIPTION') + 1] + '<br><br>';
                } else {
                    var description = '<b>DESCRIPTION</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('TYPE') >= 0) {
                    var size = '<b>SIZE</b>' + '<br>' + clientsdata[clientsdata.indexOf('TYPE') + 1] + '<br><br>';
                } else {
                    var size = '<b>SIZE</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('COPIES') >= 0) {
                    var copy = '<b>COPY</b>' + '<br>' + clientsdata[clientsdata.indexOf('COPIES') + 1] + '<br><br>';
                } else {
                    var copy = '<b>COPY</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('MAIL_PICKUP') >= 0) {
                    var mail_pickup = '<b>MAIL_PICKUP</b>' + '<br>' + clientsdata[clientsdata.indexOf('MAIL_PICKUP') + 1] + '<br><br>';
                } else {
                    var mail_pickup = '<b>MAIL_PICKUP</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                div.innerHTML = order.ship_to_name + '<br>' +
                    'Address: ' + address + ' ' + order.ship_to_city + ', ' + (order.ship_to_state == null ? '' : order.ship_to_state) +  ' ' + order.ship_to_country + ' ' + order.ship_to_zipcode + '<br>' +
                    '<h3>Photo Tax</h3>' + ordertypes +
                    '<b>Customer Name: ' + order.billingname + '</b><br>' +
                    '<b>Order Number: ' + order.orderno + '</b><br>' +
                    '<b>Time of Order: ' + order.datelastmodified + '</b><br>' +
                    '<b>Phone: ' + order.ship_to_phone + '</b><br>' +
                    '<b>Email: ' + order.customeremail + '</b><br>' +
                    '<b>SubOrderNo: ' + order.suborderno + '</b>' + '<br><br>' +
                    collection + borough + block + lot + building_number + street + description + size + copy + mail_pickup +
                    '<div class="pagebreak" style="page-break-after: always;}"></div>';
            }
            else if (order.clientagencyname == 'Photo Gallery') {
                if (clientsdata.indexOf('IMAGE_IDENTIFIER') >= 0) {
                    var image_identifier = '<b>IMAGE ID/IDENTIFIER</b>' + '<br>' + clientsdata[clientsdata.indexOf('IMAGE_IDENTIFIER') + 1] + '<br><br>';
                } else {
                    var image_identifier = '<b>IMAGE ID/IDENTIFIER</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('IMAGE_DESCRIPTION') >= 0) {
                    var description = '<b>DESCRIPTION</b>' + '<br>' + clientsdata[clientsdata.indexOf('IMAGE_DESCRIPTION') + 1] + '<br><br>';
                } else {
                    var description = '<b>DESCRIPTION</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('ADDITIONAL_DESCRIPTION') >= 0) {
                    var additional_description = '<b>ADDITIONAL_DESCRIPTION</b>' + '<br>' + clientsdata[clientsdata.indexOf('ADDITIONAL_DESCRIPTION') + 1] + '<br><br>';
                } else {
                    var additional_description = '<b>ADDITIONAL_DESCRIPTION</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('SIZE') >= 0) {
                    var size = '<b>SIZE</b>' + '<br>' + clientsdata[clientsdata.indexOf('SIZE') + 1] + '<br><br>';
                } else {
                    var size = '<b>SIZE</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('COPIES') >= 0) {
                    var copy = '<b>COPY</b>' + '<br>' + clientsdata[clientsdata.indexOf('COPIES') + 1] + '<br><br>';
                } else {
                    var copy = '<b>COPY</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('MAIL_PICKUP') >= 0) {
                    var mail_pickup = '<b>MAIL_PICKUP</b>' + '<br>' + clientsdata[clientsdata.indexOf('MAIL_PICKUP') + 1] + '<br><br>';
                } else {
                    var mail_pickup = '<b>MAIL_PICKUP</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                if (clientsdata.indexOf('PERSONAL_USE_AGREEMENT') >= 0) {
                    var personal_use_agreement = '<b>PERSONAL_USE_AGREEMENT</b>' + '<br>' + clientsdata[clientsdata.indexOf('PERSONAL_USE_AGREEMENT') + 1] + '<br><br>';
                } else {
                    var personal_use_agreement = '<b>PERSONAL_USE_AGREEMENT</b>' + '<br>' + 'N/A' + '<br><br>';
                }
                div.innerHTML = order.ship_to_name + '<br>' +
                    'Address: ' + address + ' ' + order.ship_to_city + ', ' + (order.ship_to_state == null ? '' : order.ship_to_state) +  ' ' + order.ship_to_country + ' ' + order.ship_to_zipcode + '<br>' +
                    '<h3>Photo Tax</h3>' + ordertypes +
                    '<b>Customer Name: ' + order.billingname + '</b><br>' +
                    '<b>Order Number: ' + order.orderno + '</b><br>' +
                    '<b>Time of Order: ' + order.datelastmodified + '</b><br>' +
                    '<b>Phone: ' + order.ship_to_phone + '</b><br>' +
                    '<b>Email: ' + order.customeremail + '</b><br>' +
                    '<b>SubOrderNo: ' + order.suborderno + '</b>' + '<br><br>' +
                    image_identifier + description + additional_description + size + copy + mail_pickup + personal_use_agreement +
                    '<div class="pagebreak" style="page-break-after: always;}"></div>';
            }
            document.getElementById('printorders').appendChild(div);
        }
        var orderpage = window.open();
        orderpage.document.write(document.getElementById('printorders').innerHTML);
        orderpage.print();
        orderpage.close();
        document.getElementById('printorders').innerHTML = "";
    },
    printBigLabels: function (event) {
        for (var i = 0; i < this.props.order.length; i++) {
            var div = document.createElement('div');
            div.id = 'biglabel';
            div.style.width = '50%';
            div.style.height = '20%';
            div.style.display = 'inline-block';
            div.style.fontFamily = 'Arial, Helvetica, sans-serif';
            div.style.fontSize = '14px';
            var order = this.props.order[i];
            var clientsdata = order.clientsdata.split('|');
            if (clientsdata.indexOf('CONTACT_NUMBER') >= 0) {
                var contactnumber = '<b>CONTACT_NUMBER</b>' + '<br>' +
                    clientsdata[clientsdata.indexOf('CONTACT_NUMBER') + 1] + '<br><br>';
            } else {
                var contactnumber = '';
            }
            if (order.ship_to_street_add_2 == null) {
                var address = order.ship_to_streetadd;
            } else {
                var address = order.ship_to_streetadd + ' ' + order.ship_to_street_add2;
            }
            if (order.clientagencyname == ('Photo Tax' || 'Photo Gallery')) {
                var photo_address = 'NYC DEPARTMENT OF RECORDS/MUNICIPAL ARCHIVES' + '<br>' + '31 Chambers Street' +
                    '<br>' + 'New York, NY 10007' + '<br><br>' + '<hr style="width: 95%">' + '<br>';
            } else {
                var photo_address = '';
            }
            if (order.ship_to_name.length > 1) {
                div.innerHTML = '<div style="display: table-cell; vertical-align: middle; text-align: center; width: 375px; height: 200px; margin: auto; position: relative;">' +
                    photo_address + '<b>TO: </b>' + order.ship_to_name + '<br>' + address + '<br>' + order.ship_to_city +
                    ', ' + order.ship_to_state + ' ' + order.ship_to_zipcode + ' ' + order.ship_to_country + '<br></div>';
            } else {
                div.innerHTML = '<div style="display: table-cell; vertical-align: middle; text-align: center; width: 375px; height: 200px; margin: auto; position: relative;">' +
                    'CALL FOR PICKUP' + '<br>' + order.billingname + '<br>' + contactnumber + '<br></div>';
            }
            document.getElementById('printbiglabels').appendChild(div);
        }
        var biglabelpage = window.open();
        biglabelpage.document.write(document.getElementById('printbiglabels').innerHTML);
        biglabelpage.print();
        biglabelpage.close();
        document.getElementById('printbiglabels').innerHTML = "";
    },
    printSmallLabels: function (event) {
        for (var i = 0; i < this.props.order.length; i++) {
            var div = document.createElement('div');
            div.id = 'smalllabel';
            div.style.width = '33.33%';
            div.style.height = '10%';
            div.style.display = 'inline-block';
            div.style.fontFamily = 'Arial, Helvetica, sans-serif';
            div.style.fontSize = '14px';
            var order = this.props.order[i];
            if (order.ship_to_street_add_2 == null) {
                var address = order.ship_to_streetadd;
            } else {
                var address = order.ship_to_streetadd + ' ' + order.ship_to_street_add2;
            }
            div.innerHTML = '<div style="display: table-cell; vertical-align: middle; text-align: center; width: 250px; height: 100px; margin: auto; position: relative;">' +
                order.ship_to_name + '<br>' + address + '<br>' + order.ship_to_city + ', ' + order.ship_to_state + ' ' +
                order.ship_to_zipcode + '<br></div>';
            document.getElementById('printsmalllabels').appendChild(div);
        }
        var smalllabelpage = window.open();
        smalllabelpage.document.write(document.getElementById('printsmalllabels').innerHTML);
        smalllabelpage.print();
        smalllabelpage.close();
        document.getElementById('printsmalllabels').innerHTML = "";
    },
    render: function () {
        return (
            <div className='order-wrap'>
                <h2 className='order-title'>Orders</h2>
                <ul className='order'>
                    <li className='total'>
                        <strong>Number of Items:</strong>
                        {this.props.order.length}
                        <strong>Number of Orders:</strong>
                        {this.props.uniqueOrders.length}
                        <input type="submit" name="submit" value="Print" onClick={this.printOrders}/>
                        <input type="submit" name="submit" value="Big Labels" onClick={this.printBigLabels}/>
                        <input type="submit" name="submit" value="Small Labels" onClick={this.printSmallLabels}/>
                    </li>
                    {this.props.order.map(function (order) {
                        return <li key={order.suborderno}>
                            Order #: {order.orderno}<br/>
                            Suborder #: {order.suborderno}<br/>
                            Order Type: {order.clientagencyname}<br/>
                            Billing Name: {order.billingname}<br/>
                            Date Received: {(order.datereceived).substr(0, 10)}<br/>
                        </li>
                    })}
                </ul>
            </div>
        )
    }
});

ReactDOM.render(
    <App source='/api/v1.0/orders'/>,
    document.getElementById('main')
);