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
            console.log(result.orders.length);
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
            console.log(result.orders[0])
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
 findOrder -- upon an event (apply button being clicked), an order object is created using
 information from the OrderForm and passed into the filterOrder function.
 */

var OrderForm = React.createClass({
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
                <select data-bind='value: ordertype' ref='ordertype' id='ordertype'>
                    <option disabled selected value>
                        Order Type
                    </option>
                    <option value='All'>
                        All
                    </option>
                    <option disabled value='vitalrecords'>
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
                    <option disabled value='photos'>
                        --Photos--
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
                    id='datepicker'/>
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
 */

var Order = React.createClass({
    printOrders: function (event) {
        for (var i = 0; i < this.props.order.length; i++) {
            var div = document.createElement('div');
            div.className = 'separateorder';
            var order = this.props.order[i];
            var clientsdata = order.clientsdata.split('|');
            var orderno = parseInt(order.orderno, 10);
            if (order.shiptostreetadd2 == null) {
                var address = order.shiptostreetadd;
            } else {
                var address = order.shiptostreetadd + ' ' + order.shiptostreetadd2;
            }
            var ordertypelist = order.ordertypes.split(',');
            if (ordertypelist.length > 1) {
                var ordertypes = '<b>This item was ordered with multiple items in Cart: </b>';
                if (ordertypelist.indexOf('tax photo') != -1) {
                    ordertypes += 'Photo Tax, ';
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
                div.innerHTML = order.shiptoname + '<br>' +
                    'Address: ' + address + ' ' + order.shiptocity + ', ' + order.shiptostate + ' ' + order.shiptozipcode + '<br>' +
                    '<h3>Birth Search</h3>' + ordertypes +
                    '<b>Customer Name: ' + order.billingname + '</b><br>' +
                    '<b>Order Number: ' + orderno + '</b><br>' +
                    '<b>Time of Order: ' + order.datelastmodified + '</b><br>' +
                    '<b>Phone: ' + order.shiptophone + '</b><br>' +
                    '<b>Email: ' + order.customeremail + '</b><br>' +
                    '<b>SubOrderNo: ' + order.suborderno + '</b>' + '<br><br>' +
                    '<b>LAST_NAME</b>' + '<br>' + clientsdata[clientsdata.indexOf('LASTNAME') + 1] + '<br><br>' +
                    '<b>FIRST_NAME</b>' + '<br>' + clientsdata[clientsdata.indexOf('FIRSTNAME') + 1] + '<br><br>' +
                    '<b>RELATIONSHIP</b>' + '<br>' + clientsdata[clientsdata.indexOf('RELATIONSHIP') + 1] + '<br><br>' +
                    '<b>PURPOSE</b>' + '<br>' + clientsdata[clientsdata.indexOf('PURPOSE') + 1] + '<br><br>' +
                    '<b>ADDITIONAL_COPY</b>' + '<br>' + clientsdata[clientsdata.indexOf('ADDITIONAL_COPY') + 1] + '<br><br>' +
                    '<b>BIRTH_PLACE</b>' + '<br>' + clientsdata[clientsdata.indexOf('BIRTH_PLACE') + 1] + '<br><br>' +
                    '<b>YEAR_</b>' + '<br>' + clientsdata[clientsdata.indexOf('YEAR_') + 1] + '<br><br>' +
                    '<b>BOROUGH</b>' + '<br>' + clientsdata[clientsdata.indexOf('BOROUGH') + 1] + '<br><br>' +
                    '<div class="pagebreak" style="page-break-after: always;}"></div>';
            }
            else if (order.clientagencyname == 'Marriage Search') {
                div.innerHTML = order.shiptoname + '<br>' +
                    'Address: ' + address + ' ' + order.shiptocity + ', ' + order.shiptostate + ' ' + order.shiptozipcode + '<br>' +
                    '<h3>Marriage Search</h3>' + ordertypes +
                    '<b>Customer Name: ' + order.billingname + '</b><br>' +
                    '<b>Order Number: ' + orderno + '</b><br>' +
                    '<b>Time of Order: ' + order.datelastmodified + '</b><br>' +
                    '<b>Phone: ' + order.shiptophone + '</b><br>' +
                    '<b>Email: ' + order.customeremail + '</b><br>' +
                    '<b>SubOrderNo: ' + order.suborderno + '</b>' + '<br><br>' +
                    '<b>LAST_NAME_GROOM</b>' + '<br>' + clientsdata[clientsdata.indexOf('LASTNAME_G') + 1] + '<br><br>' +
                    '<b>FIRST_NAME_GROOM</b>' + '<br>' + clientsdata[clientsdata.indexOf('FIRSTNAME_G') + 1] + '<br><br>' +
                    '<b>LAST_NAME_BRIDE</b>' + '<br>' + clientsdata[clientsdata.indexOf('LASTNAME_B') + 1] + '<br><br>' +
                    '<b>FIRST_NAME_BRIDE</b>' + '<br>' + clientsdata[clientsdata.indexOf('FIRSTNAME_B') + 1] + '<br><br>' +
                    '<b>RELATIONSHIP</b>' + '<br>' + clientsdata[clientsdata.indexOf('RELATIONSHIP') + 1] + '<br><br>' +
                    '<b>PURPOSE</b>' + '<br>' + clientsdata[clientsdata.indexOf('PURPOSE') + 1] + '<br><br>' +
                    '<b>COPY_REQ</b>' + '<br>' + clientsdata[clientsdata.indexOf('COPY_REQ') + 1] + '<br><br>' +
                    '<b>MONTH</b>' + '<br>' + clientsdata[clientsdata.indexOf('MONTH') + 1] + '<br><br>' +
                    '<b>DAY</b>' + '<br>' + clientsdata[clientsdata.indexOf('DAY') + 1] + '<br><br>' +
                    '<b>YEAR</b>' + '<br>' + clientsdata[clientsdata.indexOf('YEAR_') + 1] + '<br><br>' +
                    '<b>MARRIAGE_PLACE</b>' + '<br>' + clientsdata[clientsdata.indexOf('MARRIAGE_PLACE') + 1] + '<br><br>' +
                    '<b>BOROUGH</b>' + '<br>' + clientsdata[clientsdata.indexOf('BOROUGH') + 1] + '<br><br>' +
                    '<div class="pagebreak" style="page-break-after: always;}"></div>';
            }
            else if (order.clientagencyname == 'Death Search') {
                if (clientsdata.includes('ADD_COMMENT')) {
                    var addcomment = '<b>ADD_COMMENT</b>' + '<br>' + clientsdata[clientsdata.indexOf('ADD_COMMENT') + 1] + '<br><br>';
                } else {
                    var addcomment = '';
                }
                div.innerHTML = order.shiptoname + '<br>' +
                    'Address: ' + address + ' ' + order.shiptocity + ', ' + order.shiptostate + ' ' + order.shiptozipcode + '<br>' +
                    '<h3>Death Search</h3>' + ordertypes +
                    '<b>Customer Name: ' + order.billingname + '</b><br>' +
                    '<b>Order Number: ' + orderno + '</b><br>' +
                    '<b>Time of Order: ' + order.datelastmodified + '</b><br>' +
                    '<b>Phone: ' + order.shiptophone + '</b><br>' +
                    '<b>Email: ' + order.customeremail + '</b><br>' +
                    '<b>SubOrderNo: ' + order.suborderno + '</b>' + '<br><br>' +
                    '<b>LAST_NAME</b>' + '<br>' + clientsdata[clientsdata.indexOf('LASTNAME') + 1] + '<br><br>' +
                    '<b>FIRST_NAME</b>' + '<br>' + clientsdata[clientsdata.indexOf('FIRSTNAME') + 1] + '<br><br>' +
                    '<b>RELATIONSHIP</b>' + '<br>' + clientsdata[clientsdata.indexOf('RELATIONSHIP') + 1] + '<br><br>' +
                    '<b>COPY_REQ</b>' + '<br>' + clientsdata[clientsdata.indexOf('COPY_REQ') + 1] + '<br><br>' + addcomment +
                    '<b>YEAR</b>' + '<br>' + clientsdata[clientsdata.indexOf('YEAR_') + 1] + '<br><br>' +
                    '<b>BOROUGH</b>' + '<br>' + clientsdata[clientsdata.indexOf('BOROUGH') + 1] + '<br><br>' +
                    '<div class="pagebreak" style="page-break-after: always;}"></div>';
            }
            else if (order.clientagencyname == 'Birth Cert') {
                if (clientsdata.includes('FATHER_NAME')) {
                    var fathername = '<b>FATHER_NAME</b>' + '<br>' + clientsdata[clientsdata.indexOf('FATHER_NAME') + 1] + '<br><br>';
                } else {
                    var fathername = '<b>FATHER_NAME</b>' + '<br>' + 'Unknown' + '<br><br>';
                }
                if (clientsdata.includes('MOTHER_NAME')) {
                    var mothername = '<b>MOTHER_NAME</b>' + '<br>' + clientsdata[clientsdata.indexOf('MOTHER_NAME') + 1] + '<br><br>';
                } else {
                    var mothername = '<b>MOTHER_NAME</b>' + '<br>' + 'Unknown' + '<br><br>';
                }
                if (clientsdata.includes('BIRTH_PLACE')) {
                    var birthplace = '<b>BIRTH_PLACE</b>' + '<br>' + clientsdata[clientsdata.indexOf('BIRTH_PLACE') + 1] + '<br><br>';
                } else {
                    var birthplace = '';
                }
                div.innerHTML = order.shiptoname + '<br>' +
                    'Address: ' + address + ' ' + order.shiptocity + ', ' + order.shiptostate + ' ' + order.shiptozipcode + '<br>' +
                    '<h3>Birth Cert</h3>' + ordertypes +
                    '<b>Customer Name: ' + order.billingname + '</b><br>' +
                    '<b>Order Number: ' + orderno + '</b><br>' +
                    '<b>Time of Order: ' + order.datelastmodified + '</b><br>' +
                    '<b>Phone: ' + order.shiptophone + '</b><br>' +
                    '<b>Email: ' + order.customeremail + '</b><br>' +
                    '<b>SubOrderNo: ' + order.suborderno + '</b>' + '<br><br>' +
                    '<b>CERTIFICATE_NUMBER</b>' + '<br>' + clientsdata[clientsdata.indexOf('CERTIFICATE_NUMBER') + 1] + '<br><br>' +
                    '<b>GENDER</b>' + '<br>' + clientsdata[clientsdata.indexOf('GENDER') + 1] + '<br><br>' +
                    '<b>LAST_NAME</b>' + '<br>' + clientsdata[clientsdata.indexOf('LASTNAME') + 1] + '<br><br>' +
                    '<b>FIRST_NAME</b>' + '<br>' + clientsdata[clientsdata.indexOf('FIRSTNAME') + 1] + '<br><br>' + fathername + mothername +
                    '<b>RELATIONSHIP</b>' + '<br>' + clientsdata[clientsdata.indexOf('RELATIONSHIP') + 1] + '<br><br>' +
                    '<b>PURPOSE</b>' + '<br>' + clientsdata[clientsdata.indexOf('PURPOSE') + 1] + '<br><br>' +
                    '<b>ADDITIONAL_COPY</b>' + '<br>' + clientsdata[clientsdata.indexOf('ADDITIONAL_COPY') + 1] + '<br><br>' +
                    '<b>MONTH</b>' + '<br>' + clientsdata[clientsdata.indexOf('MONTH') + 1] + '<br><br>' +
                    '<b>DAY</b>' + '<br>' + clientsdata[clientsdata.indexOf('DAY') + 1] + '<br><br>' +
                    '<b>YEAR</b>' + '<br>' + clientsdata[clientsdata.indexOf('YEAR1') + 1] + '<br><br>' + birthplace +
                    '<b>BOROUGH</b>' + '<br>' + clientsdata[clientsdata.indexOf('BOROUGH') + 1] + '<br><br>' +
                    '<div class="pagebreak" style="page-break-after: always;}"></div>';
            }
            else if (order.clientagencyname == 'Death Cert') {
                div.innerHTML = order.shiptoname + '<br>' +
                    'Address: ' + address + ' ' + order.shiptocity + ', ' + order.shiptostate + ' ' + order.shiptozipcode + '<br>' +
                    '<h3>Death Cert</h3>' + ordertypes +
                    '<b>Customer Name: ' + order.billingname + '</b><br>' +
                    '<b>Order Number: ' + orderno + '</b><br>' +
                    '<b>Time of Order: ' + order.datelastmodified + '</b><br>' +
                    '<b>Phone: ' + order.shiptophone + '</b><br>' +
                    '<b>Email: ' + order.customeremail + '</b><br>' +
                    '<b>SubOrderNo: ' + order.suborderno + '</b>' + '<br><br>' +
                    '<b>LAST_NAME</b>' + '<br>' + clientsdata[clientsdata.indexOf('LASTNAME') + 1] + '<br><br>' +
                    '<b>FIRST_NAME</b>' + '<br>' + clientsdata[clientsdata.indexOf('FIRSTNAME') + 1] + '<br><br>' +
                    '<b>RELATIONSHIP</b>' + '<br>' + clientsdata[clientsdata.indexOf('RELATIONSHIP') + 1] + '<br><br>' +
                    '<b>PURPOSE</b>' + '<br>' + clientsdata[clientsdata.indexOf('PURPOSE') + 1] + '<br><br>' +
                    '<b>COPY_REQ</b>' + '<br>' + clientsdata[clientsdata.indexOf('COPY_REQ') + 1] + '<br><br>' +
                    '<b>MONTH</b>' + '<br>' + clientsdata[clientsdata.indexOf('MONTH') + 1] + '<br><br>' +
                    '<b>DAY</b>' + '<br>' + clientsdata[clientsdata.indexOf('DAY') + 1] + '<br><br>' +
                    '<b>YEAR</b>' + '<br>' + clientsdata[clientsdata.indexOf('YEAR') + 1] + '<br><br>' +
                    '<b>CERTIFICATE_NUMBER</b>' + '<br>' + clientsdata[clientsdata.indexOf('CERTIFICATE_NUMBER') + 1] + '<br><br>' +
                    '<b>BOROUGH</b>' + '<br>' + clientsdata[clientsdata.indexOf('BOROUGH') + 1] + '<br><br>' +
                    '<div class="pagebreak" style="page-break-after: always;}"></div>';
            }
            else if (order.clientagencyname == 'Marriage Cert') {
                div.innerHTML = order.shiptoname + '<br>' +
                    'Address: ' + address + ' ' + order.shiptocity + ', ' + order.shiptostate + ' ' + order.shiptozipcode + '<br>' +
                    '<h3>Marriage Cert</h3>' + ordertypes +
                    '<b>Customer Name: ' + order.billingname + '</b><br>' +
                    '<b>Order Number: ' + orderno + '</b><br>' +
                    '<b>Time of Order: ' + order.datelastmodified + '</b><br>' +
                    '<b>Phone: ' + order.shiptophone + '</b><br>' +
                    '<b>Email: ' + order.customeremail + '</b><br>' +
                    '<b>SubOrderNo: ' + order.suborderno + '</b>' + '<br><br>' +
                    '<b>LAST_NAME_GROOM</b>' + '<br>' + clientsdata[clientsdata.indexOf('LASTNAME_G') + 1] + '<br><br>' +
                    '<b>LAST_NAME_BRIDE</b>' + '<br>' + clientsdata[clientsdata.indexOf('LASTNAME_B') + 1] + '<br><br>' +
                    '<b>COPY_REQ</b>' + '<br>' + clientsdata[clientsdata.indexOf('COPY_REQ') + 1] + '<br><br>' +
                    '<b>YEAR</b>' + '<br>' + clientsdata[clientsdata.indexOf('YEAR') + 1] + '<br><br>' +
                    '<b>CERTIFICATE_NUMBER</b>' + '<br>' + clientsdata[clientsdata.indexOf('CERTIFICATE_NUMBER') + 1] + '<br><br>' +
                    '<b>BOROUGH</b>' + '<br>' + clientsdata[clientsdata.indexOf('BOROUGH') + 1] + '<br><br>' +
                    '<div class="pagebreak" style="page-break-after: always;}"></div>';
            }
            else if (order.clientagencyname == 'Photo Tax') {
                if (clientsdata.includes('DESCRIPTION')) {
                    var description = '<b>DESCRIPTION</b>' + '<br>' + clientsdata[clientsdata.indexOf('DESCRIPTION') + 1] + '<br><br>';
                } else {
                    var description = '';
                }
                if (clientsdata.includes('BLOCK')) {
                    var block = '<b>BLOCK</b>' + '<br>' + clientsdata[clientsdata.indexOf('BLOCK') + 1] + '<br><br>';
                } else {
                    var block = '';
                }
                if (clientsdata.includes('LOT')) {
                    var lot = '<b>LOT</b>' + '<br>' + clientsdata[clientsdata.indexOf('LOT') + 1] + '<br><br>';
                } else {
                    var lot = '';
                }
                div.innerHTML = order.shiptoname + '<br>' +
                    'Address: ' + address + ' ' + order.shiptocity + ', ' + order.shiptostate + ' ' + order.shiptozipcode + '<br>' +
                    '<h3>Photo Tax</h3>' + ordertypes +
                    '<b>Customer Name: ' + order.billingname + '</b><br>' +
                    '<b>Order Number: ' + orderno + '</b><br>' +
                    '<b>Time of Order: ' + order.datelastmodified + '</b><br>' +
                    '<b>Phone: ' + order.shiptophone + '</b><br>' +
                    '<b>Email: ' + order.customeremail + '</b><br>' +
                    '<b>SubOrderNo: ' + order.suborderno + '</b>' + '<br><br>' +
                    '<b>COLLECTION</b>' + '<br>' + clientsdata[clientsdata.indexOf('Collection') + 1] + '<br><br>' +
                    '<b>BOROUGH</b>' + '<br>' + clientsdata[clientsdata.indexOf('BOROUGH') + 1] + '<br><br>' + block + lot +
                    '<b>BUILDING_NUMBER</b>' + '<br>' + clientsdata[clientsdata.indexOf('STREET_NUMBER') + 1] + '<br><br>' +
                    '<b>STREET</b>' + '<br>' + clientsdata[clientsdata.indexOf('STREET') + 1] + '<br><br>' + description +
                    '<b>SIZE</b>' + '<br>' + clientsdata[clientsdata.indexOf('TYPE') + 1] + '<br><br>' +
                    '<b>COPY</b>' + '<br>' + clientsdata[clientsdata.indexOf('COPIES') + 1] + '<br><br>' +
                    '<b>MAIL_PICKUP</b>' + '<br>' + clientsdata[clientsdata.indexOf('MAIL_PICKUP') + 1] + '<br><br>' +
                    '<div class="pagebreak" style="page-break-after: always;}"></div>';
            }
            else if (order.clientagencyname == 'Photo Gallery') {
                if (clientsdata.includes('ADDITIONAL_DESCRIPTION')) {
                    var additionaldescription = '<b>ADDITIONAL_DESCRIPTION</b>' + '<br>' + clientsdata[clientsdata.indexOf('ADDITIONAL_DESCRIPTION') + 1] + '<br><br>';
                } else {
                    var additionaldescription = '';
                }
                div.innerHTML = order.shiptoname + '<br>' +
                    'Address: ' + address + ' ' + order.shiptocity + ', ' + order.shiptostate + ' ' + order.shiptozipcode + '<br>' +
                    '<h3>Photo Tax</h3>' + ordertypes +
                    '<b>Customer Name: ' + order.billingname + '</b><br>' +
                    '<b>Order Number: ' + orderno + '</b><br>' +
                    '<b>Time of Order: ' + order.datelastmodified + '</b><br>' +
                    '<b>Phone: ' + order.shiptophone + '</b><br>' +
                    '<b>Email: ' + order.customeremail + '</b><br>' +
                    '<b>SubOrderNo: ' + order.suborderno + '</b>' + '<br><br>' +
                    '<b>IMAGE ID/IDENTIFIER</b>' + '<br>' + clientsdata[clientsdata.indexOf('IMAGE_IDENTIFIER') + 1] + '<br><br>' +
                    '<b>DESCRIPTION</b>' + '<br>' + clientsdata[clientsdata.indexOf('IMAGE_DESCRIPTION') + 1] + '<br><br>' + additionaldescription +
                    '<b>SIZE</b>' + '<br>' + clientsdata[clientsdata.indexOf('SIZE') + 1] + '<br><br>' +
                    '<b>COPY</b>' + '<br>' + clientsdata[clientsdata.indexOf('COPIES') + 1] + '<br><br>' +
                    '<b>MAIL_PICKUP</b>' + '<br>' + clientsdata[clientsdata.indexOf('MAIL_PICKUP') + 1] + '<br><br>' +
                    '<b>PERSONAL_USE_AGREEMENT</b>' + '<br>' + clientsdata[clientsdata.indexOf('PERSONAL_USE_AGREEMENT') + 1] + '<br><br>' +
                    '<div class="pagebreak" style="page-break-after: always;}"></div>';
            }
            document.getElementById('printorders').appendChild(div);
        }
        var orderpage = window.open();
        orderpage.document.write(document.getElementById('printorders').innerHTML);
        orderpage.print();
        document.getElementById('printorders').innerHTML = "";
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
                    </li>
                    {this.props.order.map(function (order) {
                        return <li key={order.orderno}>
                            Order #: {order.clientid}<br/>
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
    <App source='http://localhost:5000/api/v1.0/orders'/>,
    document.getElementById('main')
);