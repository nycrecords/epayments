/* global $ */
import { browserHistory } from 'react-router'

var React = require('react')
var ReactDOM = require('react-dom')

var ReactRouter = require('react-router')
var Router = ReactRouter.Router
var Route = ReactRouter.Route

/*
  App
  <App />
  Return the homepage of the ePayments website. The App component includes the Inventory and Order components.
  Inventory -- tagline of 'Department of Records' and filterOrder function is passed
  Order -- state of order object and state of uniqueOrders object is passed

  Functions:
  getInitialState -- initalizes three empty lists named order, prevDayOrders, and uniqueOrders
  componentDidMount -- accesses orders from the database and updates the objects in the state
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
      uniqueOrders: []
    }
  },
  componentDidMount: function () {
    this.serverRequest = $.get(this.props.source, function (result) {
      console.log(result.orders.length)
      for (var i = 0; i < result.orders.length; i++) {
        (this.state.order).push(result.orders[i])
      }
      for (var i = 0; i < result.orders.length; i++) {
        (this.state.prevDayOrders).push(result.orders[i])
      }
      var allUniqueOrders = []
      for (var i = 0; i < this.state.order.length; i++) {
        if (allUniqueOrders.indexOf(this.state.order[i].orderno) === -1) {
          allUniqueOrders.push(this.state.order[i].orderno)
        }
      }
      this.setState({ uniqueOrders: allUniqueOrders })
    }.bind(this))
  },
  componentWillUnmount: function () {
    this.serverRequest.abort()
  },
  filterOrder: function (order) {
    console.log(order)
    this.state.order = []
    var dateRangeOrders = []
    var allUniqueOrders = []
    console.log(this.state.order)
    console.log(this.state.prevDayOrders)
    var ordernumber = order.ordernumber
    var subordernumber = order.subordernumber
    var ordertype = order.ordertype
    var billingname = order.billingname
    var datereceivedstart = order.datereceivedstart
    var datereceivedend = order.datereceivedend
    this.serverRequest = $.ajax({
      url: this.props.source,
      dataType: 'json',
      type: 'POST',
      data: {order_number: ordernumber, suborder_number: subordernumber, order_type: ordertype, billing_name: billingname, date_received_start: datereceivedstart, date_received_end: datereceivedend},
      success: function(data) {
        console.log(data.orders)
        for (var i = 0; i < data.orders.length; i++) {
          dateRangeOrders.push(data.orders[i])
        }
        this.setState({ order: dateRangeOrders })
        for (var i = 0; i < this.state.order.length; i++) {
          if (allUniqueOrders.indexOf(this.state.order[i].orderno) === -1) {
            allUniqueOrders.push(this.state.order[i].orderno)
          }
        }
        this.setState({ uniqueOrders: allUniqueOrders })
        console.log(this.state.order)
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
    console.log(this.state.order)
    var allUniqueOrders = []
    for (var i = 0; i < this.state.order.length; i++) {
      if (allUniqueOrders.indexOf(this.state.order[i].suborderno) === -1) {
        allUniqueOrders.push(this.state.order[i].suborderno)
      }
    }
    this.setState({ uniqueOrders: allUniqueOrders })
  },
  render: function () {
    return (
    <div className='epayments'>
      <Inventory tagline='Department of Records' filterOrder={this.filterOrder} />
      <Order order={this.state.order} uniqueOrders={this.state.uniqueOrders} />
    </div>
    )
  }
})

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
      <h1>ePayments Orders</h1>
      <h3 className='tagline'><span>{this.props.tagline}</span></h3>
    </header>
    )
  }
})

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
  // propTypes: {
  //   filterOrder: React.PropTypes.string.isRequired
  // },

  findOrder: function (event) {
    // Stop the form from submitting
    event.preventDefault()
    // Take data from form and create object
    var order = {
      ordernumber: this.refs.ordernumber.value,
      subordernumber: this.refs.subordernumber.value,
      ordertype: this.refs.ordertype.value,
      billingname: this.refs.billingname.value,
      datereceivedstart: this.refs.datereceivedstart.value,
      datereceivedend: this.refs.datereceivedend.value
    }
    // Search for the order(s) in database
    this.props.filterOrder(order)
  },
  render: function () {
    return (
    <form className='apply-order' ref='orderForm' onSubmit={this.findOrder}>
      <input
        data-bind='value: ordernumber'
        type='text'
        ref='ordernumber'
        placeholder='Order Number' />
      <input
        data-bind='value: subordernumber'
        type='text'
        ref='subordernumber'
        placeholder='Suborder Number' />
      <select data-bind='value: ordertype' ref='ordertype'>
        <option disabled selected value>
          Order Type
        </option>
        <option value=''>
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
        <option value='multitems'>
          Multiple Items In Cart
        </option>
        <option value='vrphoto'>
          Vital Records and Photos In Cart
        </option>
        <option value='reversal'>
          Reversal
        </option>
      </select>
      <input
        data-bind='value: billingname'
        type='text'
        ref='billingname'
        placeholder='Billing Name' />
      <input
        data-bind='value: datereceivedstart'
        type='text'
        ref='datereceivedstart'
        placeholder='Date Received - Start'
        id='datepicker' />
      <input
        data-bind='value: datereceivedend'
        type='text'
        ref='datereceivedend'
        placeholder='Date Received - End'
        id='datepicker2' />
      <button data-bind='click: findOrder' type='submit'>
        Apply
      </button>
    </form>
    )
  }
})

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
      <Header tagline={this.props.tagline} />
      <br />
      <OrderForm {...this.props} />
    </div>
    )
  }
})

/*
  Order
  <Order />
  Returns the Order component used in the App component.
  Uses the states of order and uniqueOrders passed from the App component.
*/

var Order = React.createClass({
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
        </li>
        {this.props.order.map(function (order) {
           return <li key={order.suborderno}>
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
})

ReactDOM.render(
  <App source='http://localhost:5000/api/v1.0/orders' />,
  document.getElementById('main')
)
