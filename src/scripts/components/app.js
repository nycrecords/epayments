/**
 * Created by sinsang on 4/17/17.
 */
import React from 'react';


// var App = React.createClass({
//     propTypes: {
//         source: React.PropTypes.string.isRequired
//     },
//
//     getInitialState: function () {
//         // Initalizes the state with three empty arrays called order, uniqueOrders, and orderFilters
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
export default class App extends React.Component{
    constructor(){
        super();
        this.setState = {
        // Initializes the state with three empty arrays called order, uniqueOrders, and orderFilters
            order: [], // all suborders returned from ajax call
            uniqueOrders: [], // all unique orders returned from ajax call
            orderFilters: [] // order filters when 'Apply' button is pressed
    };
    }

    componentDidMount () {
        // initial ajax called on load to set initial states
        this.serverRequest = $.get(this.props.source, function (result) {
            for (var i = 0; i < result.orders.length; i++) {
                (this.state.order).push(result.orders[i]);
            }
            var allUniqueOrders = [];
            for (i = 0; i < this.state.order.length; i++) {
                if (allUniqueOrders.indexOf(this.state.order[i].orderno) === -1) {
                    allUniqueOrders.push(this.state.order[i].orderno)
                }
            }
            this.state({uniqueOrders: allUniqueOrders});
        }.bind(this))
    }

    componentWillUnmount () {
        // performs cleanup of DOM elements created in componentDidMount before a component is unmounted
        this.serverRequest.abort()
    }

    filterOrder (order) {
        // function is called from findOrder() in the OrderForm component
        // ajax call that passes back a dictionary containing the fields of the order form to retrieve filtered orders
        this.state.order = [];
        var dateRangeOrders = [];
        var allUniqueOrders = [];
        var orderNumber = order.orderNumber;
        var subOrderNumber = order.subOrderNumber;
        var orderType = order.orderType;
        var billingName = order.billingName;
        var dateReceivedStart = order.dateReceivedStart;
        var dateReceivedEnd = order.dateReceivedEnd;
        if (Date.parse(dateReceivedStart) > Date.parse(dateReceivedEnd)) {
            alert("Invalid Date Range: 'Date Received - Start' cannot be after 'Date Received - End'.")
        }
        this.serverRequest = $.ajax({
            url: this.props.source,
            dataType: 'json',
            type: 'POST',
            data: {
                order_number: orderNumber,
                suborder_number: subOrderNumber,
                order_type: orderType,
                billing_name: billingName,
                date_received_start: dateReceivedStart,
                date_received_end: dateReceivedEnd
            },
            success: function (data) {
                for (var i = 0; i < data.orders.length; i++) {
                    dateRangeOrders.push(data.orders[i])
                }
                this.setState({order: dateRangeOrders});
                for (i = 0; i < this.state.order.length; i++) {
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
    }

    render() {
        return (
            <div className='epayments'>
                <Inventory tagline='Department of Records' filterOrder={this.filterOrder}
                           orderFilters={this.state.orderFilters}/>
                <Order order={this.state.order} uniqueOrders={this.state.uniqueOrders}
                       orderFilters={this.state.orderFilters}/>
            </div>
        )
    }
}

App.propTypes = {
        source: React.PropTypes.string.isRequired
    };
