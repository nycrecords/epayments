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
      // console.log(result.orders)
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
    for (var i = 0; i < this.state.prevDayOrders.length; i++) {
      filteredOrders.push(this.state.prevDayOrders[i])
    }
    console.log(filteredOrders)
    for (var i = filteredOrders.length - 1; i > -1; i--) {
      console.log(i)
      if (order.ordernumber.length > 0) {
        if (order.ordernumber != (filteredOrders[i].orderno).toString()) {
          console.log(1)
          filteredOrders.splice(i, 1)
          continue
        }
      }
      if (order.subordernumber.length > 0) {
        if (order.subordernumber != (filteredOrders[i].suborderno).toString()) {
          console.log(2)
          filteredOrders.splice(i, 1)
          continue
        }
      }
      if (order.ordertype.length != 4) {
        console.log(filteredOrders[i])
        if (order.ordertype != (filteredOrders[i].clientagencyname)) {
          console.log(3)
          filteredOrders.splice(i, 1)
          continue
        }
      }
      if (order.name.length > 0) {
        if (order.name != (filteredOrders[i].billingname).toString()) {
          console.log(4)
          filteredOrders.splice(i, 1)
          continue
        }
      }
      // if (order.datereceived.length > 0) {
        // #AJAX Call
      // }
      // if (order.datelastmodified != ((this.state.prevDayOrders[i].datelastmodified).toString()).substr(0, 9) && order.datelastmodified.length > 0) {
      //   filteredOrders.splice(i, 1)
      //   console.log(5)
      //   continue
      // }
      // if (order.datereceived != (this.state.prevDayOrders[i].datereceived).toString() && order.datereceived.length > 0) {
      //   filteredOrders.splice(i, 1)
      //   console.log(6)
      //   continue
      // }
    }
    console.log(filteredOrders)
    this.setState({ order: filteredOrders })
    var allUniqueOrders = []
    for (var i = 0; i < filteredOrders.length; i++) {
      if (allUniqueOrders.indexOf(filteredOrders[i].orderno) === -1) {
        allUniqueOrders.push(filteredOrders[i].orderno)
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
  OrderForm includes a field for Order Number, Sub Order Number, Order Type, Name, Date Start, and Date End.
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
      name: this.refs.name.value,
      datelastmodified: this.refs.datelastmodified.value,
      datereceived: this.refs.datereceieved.value
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
                    {order.BillingName}
                  </li>
         })}
      </ul>
    </div>
    )
  }
})

ReactDOM.render(
  <App source='http://localhost:5000/api/v1.0' />,
  document.getElementById('main')
)
