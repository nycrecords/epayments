import { browserHistory } from 'react-router'

var React = require('react');
var ReactDOM = require('react-dom');

var ReactRouter = require('react-router');
var Router  = ReactRouter.Router;
var Route = ReactRouter.Route;
var History = ReactRouter.History;
// var createBrowserHistory = require('history/lib/createBrowserHistory');

var h = require('./helpers');


/*
  App
  <App />
*/

var App = React.createClass({
  getInitialState : function() {
    return {
      order : {}
    }
  },
  componentDidMount: function() {
    this.serverRequest = $.get(this.props.source, function(result) {
      this.state.order = result.orders;
      console.log(this.state.order);
      // this.setState({ order : order });
      // for (var i = 0; i < order.length; i++) {
      //   this.setState({ order : order[i] })
      //   this.state.order.list.push({ order : order[i] });
      // }
      // console.log(this.state.order);
    }.bind(this));
  },
  componentWillUnmount: function() {
    this.serverRequest.abort();
  },
  filterOrder : function(order) {
    // console.log(order.ordernumber);
    // console.log(this.state.order.OrderNo);
    console.log(order);
    console.log(this.state.order);
    for (var i = 0; i < this.state.order.length; i++) {
      console.log(this.state.order[i].OrderNo);
      console.log(order.ordernumber);
      if (order.ordernumber === (this.state.order[i].OrderNo).toString()) {
        console.log(1);
        this.setState({ order : order });
        console.log(this.state.order);
      } else if (order.subordernumber === (this.state.order[i].OrderNo).toString()) {
        console.log(2);
        this.setState({ order : order });
      } else if (order.ordertype === (this.state.order[i].ClientAgencyName).toString()) {
        console.log(3);
        this.setState({ order : order });
      } else if (order.name === (this.state.order[i].BillingName).toString()) {
        console.log(4);
        this.setState({ order : order });
      } else if (order.date === (this.state.order[i].DateReceived).toString()) {
        console.log(5);
        this.setState({ order : order });
      }
    }
  },
  render : function() {
    return (
      <div className="epayments">
        <Inventory tagline="Department of Records" filterOrder={this.filterOrder} />
        <Order {...this.props} />
      </div>
    )
  }
});


/*
  Header
  <Header />
*/

var Header = React.createClass({
  render : function() {
    return (
      <header className="top">
        <h1>ePayments Orders</h1>
        <h3 className="tagline"><span>{this.props.tagline}</span></h3> 
      </header>
    )
  }
});


/*
  OrderForm
  <OrderForm />
*/

var OrderForm = React.createClass({
  findOrder : function(event) {
    // Stop the form from submitting
    event.preventDefault();
    // Take data from form and create object
    var order = {
      ordernumber : this.refs.ordernumber.value,
      subordernumber : this.refs.subordernumber.value,
      ordertype : this.refs.ordertype.value,
      name : this.refs.name.value,
      date : this.refs.date.value
    }
    // Search for the order(s) in database
    console.log(order);
    this.props.filterOrder(order);
  },
  render : function() {
    return (
      <form className="apply-order" ref="orderForm" onSubmit={this.findOrder}>
        <input data-bind="value: ordernumber" type="text" ref="ordernumber" placeholder="Order Number"/>
        <input data-bind="value: subordernumber" type="text" ref="subordernumber" placeholder="Sub Order Number" />
        <select data-bind="value: ordertype" ref="ordertype">
          <option disabled selected value>Order Type</option>
          <option value="all">All</option>
          <option disabled value="vitalrecords">--Vital Records--</option>
          <option value="birthsearch">Birth Search</option>
          <option value="marriagesearch">Marriage Search</option>
          <option value="deathsearch">Death Search</option>
          <option value="birthcert">Birth Certificate</option>
          <option value="marriagecert">Marriage Certificate</option>
          <option value="deathcert">Death Certificate</option>
          <option disabled value="photos">--Photos--</option>
          <option value="phototax">Photo Tax</option>
          <option value="photogallery">Photo Gallery</option>
          <option disabled value="other">--Other--</option>
          <option value="multitems">Multiple Items In Cart</option>
          <option value="vrphoto">Vital Records and Photos In Cart</option>
          <option value="reversal">Reversal</option>
        </select>
        <input data-bind="value: name" type="text" ref="name" placeholder="Name" />
        <input data-bind="value: date" type="text" ref="date" placeholder="Date" id="datepicker" />
        <button data-bind="click: findOrder" type="submit"> Apply </button>
      </form>
    )
  }
});


/*
  Inventory
  <Inventory />
*/

var Inventory = React.createClass({
  render : function() {
    return (
      <div>
        <Header tagline={this.props.tagline} />
        <br/>
        <OrderForm {...this.props} />
      </div>
    )
  }
});


/*
  Order
  <Order />
*/

var Order = React.createClass({
  render : function() {
    // orderIds are all the orders
    // var orderIds = Object.keys(this.props.order);
    // console.log(orderIds);
    // console.log(this.props.order.ordernumber);
    // var items = Find total items
    // var orders = Find total orders
    // {orderIds.map(this.renderOrder
    // console.log(this.props.order);
    return (
      <div className="order-wrap">
      <h2 className="order-title">Orders</h2>
      <ul className="order">
        <li className="total">
          <strong>Number of Items:</strong>
          0
          <strong>Number of Orders:</strong>
          0
        </li><br/>
      </ul>
      </div>
    )
  }
})


/*
  Not Found
*/

var NotFound = React.createClass({
  render : function() {
    return <h1>Not Found!</h1>
  }
});


/*
  Routes
*/

var routes = (
  <Router history={browserHistory}>
    <Route path="/" component={App}/>
    <Route path="*" component={NotFound}/>
  </Router>
)

// ReactDOM.render(routes, document.querySelector('#main'));
ReactDOM.render(
  <App source="http://localhost:5000/epayments/api/v1.0/orders" />,
  document.getElementById('main')
);

/*
  App
*/

// var App = React.createClass({
//   getInitialState : function() {
//    return {
//      ordernumber : '',
//      subordernumber : '',
//      ordertype : '',
//      name : '',
//      date : ''
//    };
//   },
//   handleChange : function() {
//    this.setState({
//      ordernumber : this.refs.ordernumber.value,
//      subordernumber : this.refs.subordernumber.value,
//      ordertype : this.refs.ordertype.value,
//      name : this.refs.name.value,
//      date : this.refs.date.value
//    });
//   },
//   render : function() {
//    return (
//      <div className="epayments">
//      <div>
//         <header className="top">
//         <h1>ePayments Orders</h1>
//         <h3 className="tagline"><span>Department of Records</span></h3>
//         </header>
//         <br/>
//      <form className="apply-order" ref="orderForm">
//         <input type="text" ref="ordernumber" placeholder="Order Number"/>
//         <input type="text" ref="subordernumber" placeholder="Sub Order Number" />
//         <select ref="ordertype">
//           <option disabled selected value>Order Type</option>
//           <option value="all">All</option>
//           <option disabled value="vitalrecords">--Vital Records--</option>
//           <option value="birthsearch">Birth Search</option>
//           <option value="marriagesearch">Marriage Search</option>
//           <option value="deathsearch">Death Search</option>
//           <option value="birthcert">Birth Certificate</option>
//           <option value="marriagecert">Marriage Certificate</option>
//           <option value="deathcert">Death Certificate</option>
//           <option disabled value="photos">--Photos--</option>
//           <option value="phototax">Photo Tax</option>
//           <option value="photogallery">Photo Gallery</option>
//           <option disabled value="other">--Other--</option>
//           <option value="multitems">Multiple Items In Cart</option>
//           <option value="vrphoto">Vital Records and Photos In Cart</option>
//           <option value="reversal">Reversal</option>
//         </select>
//         <input type="text" ref="name" placeholder="Name" />
//         <input type="text" ref="date" placeholder="Date" id="datepicker" />
//         <button type="submit"> Apply </button>
//       </form>
//       </div>
//       <div className="order-wrap">
//      <h2 className="order-title">Orders</h2>
//      <ul className="order">
//        <li className="total">
//          <strong>Number of Items:</strong>
//          0
//          <strong>Number of Orders:</strong>
//          0
//        </li>
//      </ul>
//       </div>
//       </div>
//    );
//   }
// });

// var App = React.createClass({
//   getInitialState : function() {
//    return {
//      order : {}
//    }
//   },
//   filterOrder : function(order) {
//    // update the state object
//    this.state.order = order;
//    // set the state
//    this.setState({ order : this.state.order });
//   },
//   render : function() {
//     return (
//       <div className="epayments">
//         <Inventory tagline="Department of Records" searchOrder={this.searchOrder} filterOrder={this.filterOrder} />
//         <Order order={this.state.order} />
//       </div>
//     )
//   }
// });


// /*
//  Search Order Form
//  <SearchOrdersForm />
// */

// var SearchOrdersForm = React.createClass({
//   searchOrder : function(event) {
//    // 1. Stop the form from submitting
//    event.preventDefault();
//    // 2. Take the data from the form and create an object
//    var order = {
//      ordernumber : this.refs.ordernumber.value,
//      subordernumber : this.refs.subordernumber.value,
//      ordertype : this.refs.ordertype.value,
//      name : this.refs.name.value,
//      date : this.refs.date.value
//    }
//    console.log(order);
//    // 3. Search for the order in the database
//    // Find the order
//    this.props.filterOrder(order);
//   },
  // render : function() {
  //  return (
  //    <form className="apply-order" ref="orderForm" onSubmit={this.searchOrder}>
  //       <input type="text" ref="ordernumber" placeholder="Order Number"/>
  //       <input type="text" ref="subordernumber" placeholder="Sub Order Number" />
  //       <select ref="ordertype">
  //         <option disabled selected value>Order Type</option>
  //         <option value="all">All</option>
  //         <option disabled value="vitalrecords">--Vital Records--</option>
  //         <option value="birthsearch">Birth Search</option>
  //         <option value="marriagesearch">Marriage Search</option>
  //         <option value="deathsearch">Death Search</option>
  //         <option value="birthcert">Birth Certificate</option>
  //         <option value="marriagecert">Marriage Certificate</option>
  //         <option value="deathcert">Death Certificate</option>
  //         <option disabled value="photos">--Photos--</option>
  //         <option value="phototax">Photo Tax</option>
  //         <option value="photogallery">Photo Gallery</option>
  //         <option disabled value="other">--Other--</option>
  //         <option value="multitems">Multiple Items In Cart</option>
  //         <option value="vrphoto">Vital Records and Photos In Cart</option>
  //         <option value="reversal">Reversal</option>
  //       </select>
  //       <input type="text" ref="name" placeholder="Name" />
  //       <input type="text" ref="date" placeholder="Date" id="datepicker" />
  //       <button type="submit"> Apply </button>
  //     </form>
  //  )
//   }
// });


// /*
//   Inventory
//   <Inventory/>
// */
// var Inventory = React.createClass({
//   render : function() {
//     return (
//       <div>
//         <header className="top">
//         <h1>ePayments Orders</h1>
//         <h3 className="tagline"><span>{this.props.tagline}</span></h3>
//         </header>
//         <br/>
//         <SearchOrdersForm {...this.props} />
//       </div>
//     )
//   }
// })


// /*
//   Order
//   <Order/>
// */
// var Order = React.createClass({
//   renderOrder : function(key) {
//    // Orders in the database
//    var singleOrder = this.props.order[key];
//    if (!singleOrder) {
//      return <li>There are no orders.</li>
//    }
//    return (
//      <li>
//        {singleOrder.name}
//      </li>
//    )
//   },
//   render : function() {
//    // orderIds are all the orders
//    var orderIds = Object.keys(this.props.order);
//    // var items = Find total items
//    // var orders = Find total orders
//     return (
//       <div className="order-wrap">
//      <h2 className="order-title">Orders</h2>
//      <ul className="order">
//      {orderIds.map(this.renderOrder)}
//        <li className="total">
//          <strong>Number of Items:</strong>
//          0
//          <strong>Number of Orders:</strong>
//          0
//        </li>
//      </ul>
//       </div>
//     )
//   }
// })
