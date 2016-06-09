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
  TODO: Insert comment here explaining the App component
*/
var App = React.createClass({
  propTypes: {
    source: React.PropTypes.string.isRequired
  },

  getInitialState: function () {
    return {
      order: [],
      allOrders : []
    }
  },
  componentDidMount: function () {
    this.serverRequest = $.get(this.props.source, function (result) {
      // var allOrders = []
      for (var i = 0; i < result.orders.length; i++) {
        (this.state.allOrders).push(result.orders[i])
      }
      this.setState({ order : this.state.allOrders })
      console.log(this.state.order)
      console.log(this.state.allOrders)
    }.bind(this))
  },
  componentWillUnmount: function () {
    this.serverRequest.abort()
  },
  filterOrder: function (order) {
    console.log(order)
    // Modify datelastmodified to match database value
    if ((parseInt(order.datelastmodified.substr(0, 2))) < 10) {
      // 0#/##/## --> #/##/##
      order.datelastmodified = order.datelastmodified.substr(1, 9)
      if ((parseInt(order.datelastmodified.substr(2, 2))) < 10) {
      // #/0#/## --> #/#/##
      order.datelastmodified = (order.datelastmodified.substr(0, 2) + order.datelastmodified.substr(3, 6))
      }
    }
    if (!((parseInt(order.datelastmodified.substr(0, 1))) < 10)) {
      if ((parseInt(order.datelastmodified.substr(2, 2))) < 10) {
      // ##/0#/## --> ##/#/##
        order.datelastmodified = (order.datelastmodified.substr(0, 3) + order.datelastmodified.substr(4, 6))
      }
    }
    var filteredOrders = []
    for (var i = 0; i < this.state.allOrders.length; i++) {
      if (order.ordernumber === (this.state.allOrders[i].OrderNo).toString()) {
        console.log(1)
        filteredOrders.push(this.state.allOrders[i])
        console.log(this.state.order)
      } else if (order.subordernumber === ((this.state.allOrders[i].uri).toString()).substr(48, 10)) {
        console.log(2)
        filteredOrders.push(this.state.allOrders[i])
      } else if (order.ordertype === (this.state.allOrders[i].ClientAgencyName).toString()) {
        console.log(3)
        filteredOrders.push(this.state.allOrders[i])
      } else if (order.name === (this.state.allOrders[i].BillingName).toString()) {
        console.log(4)
        filteredOrders.push(this.state.allOrders[i])
      } else if (order.datelastmodified === ((this.state.allOrders[i].DateLastModified).toString()).substr(0, 9)) {
        console.log(5)
        console.log((this.state.allOrders[i].DateLastModified).toString())
        filteredOrders.push(this.state.allOrders[i])
      } else if (order.datereceived === (this.state.allOrders[i].DateReceived).toString()) {
        console.log(6)
        filteredOrders.push(this.state.allOrders[i])
      }
    }
    this.setState({ order : filteredOrders })
    console.log(this.state.order)
  },
  render: function () {
    return (
    <div className='epayments'>
      <Inventory tagline='Department of Records' filterOrder={this.filterOrder} />
      <Order order={this.state.order} />
    </div>
    )
  }
})

/*
  Header
  <Header />
  TODO: Insert comment here explaining the Header component
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
  TODO: Insert comment here explaining the OrderForm component
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
      name: this.refs.name.value,
      datelastmodified: this.refs.datelastmodified.value,
      datereceived: this.refs.datereceieved.value
    }
    // Search for the order(s) in database
    console.log(order)
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
        placeholder='Sub Order Number' />
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
        data-bind='value: name'
        type='text'
        ref='name'
        placeholder='Name' />
      <input
        data-bind='value: datelastmodified'
        type='text'
        ref='datelastmodified'
        placeholder='Date Last Modified'
        id='datepicker' />
      <input
        data-bind='value: datereceived'
        type='text'
        ref='datereceieved'
        placeholder='Date Received'
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
  TODO: Insert comment here explaining the Inventory component
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
  TODO: Insert comment here explaining the Order component
*/

var Order = React.createClass({
  render: function () {
    console.log(this.props.order)
    return (
    <div className='order-wrap'>
      <h2 className='order-title'>Orders</h2>
      <ul className='order'>
        <li className='total'>
          <strong>Number of Items:</strong> 0
          <strong>Number of Orders:</strong> {this.props.order.length}
        </li>
        {this.props.order.map(function(order) {
          return <li key={order.uri}>{order.BillingName}</li>})}
      </ul>
    </div>
    )
  }
})


/*
  Not Found
  TODO: Insert comment here explaining the Not Found component
*/

var NotFound = React.createClass({
  render: function () {
    return <h1>Not Found!</h1>
  }
})

/*
  Routes
  TODO: Insert comment here explaining the Routes component

  Why is this here if it isn't used?
*/

var routes = (
<Router history={browserHistory}>
  <Route path='/' component={App} />
  <Route path='*' component={NotFound} />
</Router>
)

ReactDOM.render(
  <App source='http://localhost:5000/epayments/api/v1.0/orders' />,
  document.getElementById('main')
)
