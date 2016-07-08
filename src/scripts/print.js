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
  Return the print orders page of the ePayments website. The App component includes the BirthSearch component.

  Functions:
  getInitialState -- initalizes three empty lists named birthSearchOrders, marriageSearchOrders, deathSearchOrders,
  					 birthCertOrders, marriageCertOrders, deathCertOrders, photoTaxOrders, and photoTaxOrders
  componentDidMount -- accesses orders from the database and updates the objects in the state
  componentWillUnmount -- throws an error if data is not received successfully
*/

var App = React.createClass({
  getInitialState: function () {
    return {
      birthSearchOrders: [],
      marriageSearchOrders: [],
      deathSearchOrders: [],
      birthCertOrders: [],
      marriageCertOrders: [],
      deathCertOrders: [],
      photoTaxOrders: [],
      photoGalleryOrders: []
    }
  },
  componentDidMount: function () {
    this.serverRequest = $.get(this.props.source, function (result) {
      console.log(result.orders.length)
      console.log(this.state.order)
      for (var i = 0; i < result.orders.length; i++) {
        if (result.orders[i].clientagencyname == "BirthSearch") {
        	(this.state.birthSearchOrders).push(result.orders[i])
        }
        else if (result.orders[i].clientagencyname == "MarriageSearch") {
        	(this.state.marriageSearchOrders).push(result.orders[i])
        }
        else if (result.orders[i].clientagencyname == "DeathSearch") {
        	(this.state.deathSearchOrders).push(result.orders[i])
        }
        else if (result.orders[i].clientagencyname == "BirthCert") {
        	(this.state.birthCertOrders).push(result.orders[i])
        }
        else if (result.orders[i].clientagencyname == "MarriageCert") {
        	(this.state.marriageCertOrders).push(result.orders[i])
        }
        else if (result.orders[i].clientagencyname == "DeathCert") {
        	(this.state.deathCertOrders).push(result.orders[i])
        }
        else if (result.orders[i].clientagencyname == "PhotoTax") {
        	(this.state.photoTaxOrders).push(result.orders[i])
        }
        else if (result.orders[i].clientagencyname == "PhotoGallery") {
        	(this.state.photoGalleryOrders).push(result.orders[i])
        }
      }
    }.bind(this))
  },
  componentWillUnmount: function () {
    this.serverRequest.abort()
  },
  render: function () {
    return (
      <div className='epayments'>
      	<BirthSearch birthSearchOrders={this.state.birthSearchOrders} />
      </div>
    )
  }
})

/*
  BirthSearch
  <BirthSearch />
  Return the BirthSearch component.
  Uses the birthSearchOrders state passed from the App component.
*/

var BirthSearch = React.createClass({
  render: function() {
	return (
	  <div className='order-wrap'>
    	{this.props.birthSearchOrders.map(function (order) {
           return <li key={order.suborderno}>
		              {order.billingname}<br/>
		              {order.shiptostreetadd}<br/>
		              {order.shiptocity}, {order.shiptostate} {order.shiptozipcode}<br/>
		              <br/>
		              {order.clientagencyname}<br/>
		              <br/>
		              Customer Name: {order.billingname}<br/>
		              Order Number: {order.orderno}<br/>
		              Time of Order: {order.datelastmodified}<br/>
		              Phone: {order.shiptophone}<br/>
		              Email: {order.customeremail}<br/>
		              <br/>
		              SubOrderNo: {order.suborderno}<br/>
		              <br/>
		              LASTNAME<br/>
		              {order.clientsdata.split('|')[11]}<br/>
		              <br/>
		              FIRSTNAME<br/>
		              {order.clientsdata.split('|')[13]}<br/>
		              <br/>
		              RELATIONSHIP<br/>
		              {order.clientsdata.split('|')[19]}<br/>
		              <br/>
		              PURPOSE<br/>
		              {order.clientsdata.split('|')[21]}<br/>
		              <br/>
		              COPY_REQ<br/>
		              {order.clientsdata.split('|')[23]}<br/>
		              <br/>
		              MONTH<br/>
		              {order.clientsdata.split('|')[25]}<br/>
		              <br/>
		              DAY<br/>
		              {order.clientsdata.split('|')[27]}<br/>
		              <br/>
		              YEAR<br/>
		              {order.clientsdata.split('|')[31]}<br/>
		              <br/>
		           </li>
        })}
      </div>
	)
  }
})

ReactDOM.render(
  <App source='http://localhost:5000/api/v1.0/orders' />,
  document.getElementById('main')
)
