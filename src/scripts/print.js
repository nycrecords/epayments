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
      console.log(result.orders)
      for (var i = 0; i < result.orders.length; i++) {
        if (result.orders[i].clientagencyname == "Birth Search") {
        	(this.state.birthSearchOrders).push(result.orders[i])
        }
        else if (result.orders[i].clientagencyname == "Marriage Search") {
        	(this.state.marriageSearchOrders).push(result.orders[i])
        }
        else if (result.orders[i].clientagencyname == "Death Search") {
        	(this.state.deathSearchOrders).push(result.orders[i])
        }
        else if (result.orders[i].clientagencyname == "Birth Cert") {
        	(this.state.birthCertOrders).push(result.orders[i])
        }
        else if (result.orders[i].clientagencyname == "Marriage Cert") {
        	(this.state.marriageCertOrders).push(result.orders[i])
        }
        else if (result.orders[i].clientagencyname == "Death Cert") {
        	(this.state.deathCertOrders).push(result.orders[i])
        }
        else if (result.orders[i].clientagencyname == "Photo Tax") {
        	(this.state.photoTaxOrders).push(result.orders[i])
        }
        else if (result.orders[i].clientagencyname == "Photo Gallery") {
        	(this.state.photoGalleryOrders).push(result.orders[i])
        }
      }
      this.setState({ birthSearchOrders: this.state.birthSearchOrders })
      this.setState({ marriageSearchOrders: this.state.marriageSearchOrders })
      this.setState({ deathSearchOrders: this.state.deathSearchOrders })
      this.setState({ birthCertOrders: this.state.birthCertOrders })
      this.setState({ marriageCertOrders: this.state.marriageCertOrders })
      this.setState({ deathCertOrders: this.state.deathCertOrders })
      this.setState({ photoTaxOrders: this.state.photoTaxOrders })
      this.setState({ photoGalleryOrders: this.state.photoGalleryOrders })
      console.log(this.state.birthSearchOrders)
    }.bind(this))
  },
  componentWillUnmount: function () {
    this.serverRequest.abort()
  },
  render: function () {
    return (
      <div>
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
           return <ul key={order.suborderno}>
           	<div className="pagebreak">
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
             {order.clientsdata.split('|')[9]}<br/>
             <br/>
             FIRSTNAME<br/>
             {order.clientsdata.split('|')[11]}<br/>
             <br/>
             RELATIONSHIP<br/>
             {order.clientsdata.split('|')[17]}<br/>
             <br/>
             PURPOSE<br/>
             {order.clientsdata.split('|')[19]}<br/>
             <br/>
             COPY_REQ<br/>
             {order.clientsdata.split('|')[21]}<br/>
             <br/>
             MONTH<br/>
             {order.clientsdata.split('|')[23]}<br/>
             <br/>
             DAY<br/>
             {order.clientsdata.split('|')[25]}<br/>
             <br/>
             YEAR<br/>
             {order.clientsdata.split('|')[27]}<br/>
             <br/>
           </div>
          </ul>
        })}
      </div>
	)
  }
})

ReactDOM.render(
  <App source='http://localhost:5000/api/v1.0/orders' />,
  document.getElementById('main')
)
