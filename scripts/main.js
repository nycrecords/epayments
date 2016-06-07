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
      order: []
    }
  },
  componentDidMount: function () {
    this.serverRequest = $.get(this.props.source, function (result) {
      var allOrders = []
      for (var i = 0; i < result.orders.length; i++) {
        allOrders.push(result.orders[i])
      }
      this.setState({ order : allOrders })
      console.log(this.state.order)
      console.log(allOrders)
    }.bind(this))
  },
  componentWillUnmount: function () {
    this.serverRequest.abort()
  },
  filterOrder: function (order) {
    console.log(order)
    console.log(this.state.order)
    for (var i = 0; i < this.state.order.length; i++) {
      console.log(this.state.order[i].OrderNo)
      console.log(order.ordernumber)
      if (order.ordernumber === (this.state.order[i].OrderNo).toString()) {
        console.log(1)
        this.setState({ order: order })
        console.log(this.state.order)
      } else if (order.subordernumber === (this.state.order[i].OrderNo).toString()) {
        console.log(2)
        this.setState({ order: order })
      } else if (order.ordertype === (this.state.order[i].ClientAgencyName).toString()) {
        console.log(3)
        this.setState({ order: order })
      } else if (order.name === (this.state.order[i].BillingName).toString()) {
        console.log(4)
        this.setState({ order: order })
      } else if (order.date === (this.state.order[i].DateReceived).toString()) {
        console.log(5)
        this.setState({ order: order })
      }
    }
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
      date: this.refs.date.value
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
        <option value='all'>
          All
        </option>
        <option disabled value='vitalrecords'>
          --Vital Records--
        </option>
        <option value='birthsearch'>
          Birth Search
        </option>
        <option value='marriagesearch'>
          Marriage Search
        </option>
        <option value='deathsearch'>
          Death Search
        </option>
        <option value='birthcert'>
          Birth Certificate
        </option>
        <option value='marriagecert'>
          Marriage Certificate
        </option>
        <option value='deathcert'>
          Death Certificate
        </option>
        <option disabled value='photos'>
          --Photos--
        </option>
        <option value='phototax'>
          Photo Tax
        </option>
        <option value='photogallery'>
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
        data-bind='value: date'
        type='text'
        ref='date'
        placeholder='Date'
        id='datepicker' />
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
          return <li key={order.ClientAgencyName}>{order.BillingName}</li>})}
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
