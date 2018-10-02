import React from 'react';
import {Link} from "react-router-dom";
import {Button, Container, Dimmer, Grid, Header, Icon, Loader, Rail, Segment} from 'semantic-ui-react';
import {connect} from 'react-redux';
import {mapDispatchToProps, mapStateToProps} from "../utils/reduxMappers";
import OrderForm from "./order_form";
import Order from "./order";
import LoginModal from "./login_modal";
import {csrfFetch, handleFetchErrors} from "../utils/fetch"
import {CHUNK_SIZE} from "../constants/constants"

/***
 * Custom Classes from index.css Starts with '-'; Overrides Bootstrap css and Semantic ui css
 */


class Home extends React.Component {
    constructor() {
        super();

        this.state = {
            all_orders: [],
            order_count: 0,
            suborder_count: 0,
            loading: false,
            showCSVButton: false,
            suborder_two: 0
        };

        this.addOrder = (order_count, suborder_count, orders, firstTime) => {
            if (firstTime) {
                this.setState({
                    all_orders: orders,
                    order_count: order_count,
                    suborder_count: suborder_count,
                    suborder_two: CHUNK_SIZE,
                });
                this.div.scrollTop = 0;
            } else {
                this.setState((prevState) => {
                    return {
                        all_orders: prevState.all_orders.concat(orders),
                        suborder_two: prevState.suborder_two + CHUNK_SIZE
                    };
                });
            }
        };

        this.updateStatus = (suborder_number, new_status) => {
            let status_obj = this.state.all_orders.find(obj => {
                return obj.suborder_number === suborder_number;
            });
            let idx = this.state.all_orders.indexOf(status_obj);
            let status = {"index": idx, "object": status_obj};
            status.object.current_status = new_status;
            let _all_orders = this.state.all_orders.slice();
            _all_orders[status.index] = status.object;
            this.setState({all_orders: _all_orders});
        };

        this.setLoadingState = (loading) => {
            this.setState({
                loading: loading
            });
        };

        this.loadMore = (e) => {
            this.setLoadingState(true);
            this.orderForm.setStartSize(e);
            // this.orderForm.submitFormData(e, 'load_more');
        };

        this.generateCSV = (e) => {
            this.setLoadingState(true);
            this.orderForm.submitFormData(e, 'csv');
        };

        this.printOrderSheet = (e) => {
            this.setLoadingState(true);
            this.orderForm.submitFormData(e, 'orders')
        };

        this.printBigLabels = (e) => {
            this.setLoadingState(true);
            this.orderForm.submitFormData(e, 'large_labels')
        };

        this.printSmallLabels = (e) => {
            this.setLoadingState(true);
            this.orderForm.submitFormData(e, 'small_labels')
        };

        this.logOut = () => {
            this.setLoadingState(true);
            csrfFetch('api/v1.0/logout', {
                method: "DELETE",
            })
                .then(handleFetchErrors)
                .then((json) => {
                    if (json.authenticated === false) {
                        this.props.logout();
                        alert("Logged Out");
                    }
                }).catch((error) => {
                console.error(error);
                this.props.authenticated && this.props.logout();
                this.setLoadingState(false);
            });
        };
    };

    handleListChange = (name, value, state, index) => {
        let newState = state.slice();
        newState[index] = value;
        this.setState({
            [name]: newState
        });
    };

    toggleCSV = (visible) => {
        this.setState({showCSVButton: visible});
    };

    getOrders() {
        csrfFetch('api/v1.0/orders')
            .then(response => {
                // check response status to logout user if backend session expired
                switch (response.status) {
                    case 500:
                        throw Error(response.statusText);
                    case 401:
                        this.props.authenticated && this.props.logout();
                        throw Error(response.statusText);
                    case 200:
                        return response.json();
                    default:
                        throw Error("Unhandled HTTP status code");
                }
            })
            .then((json) => {
                this.addOrder(json.order_count, json.suborder_count, json.all_orders, true);
            }).catch((error) => {
            console.error(error);
        });
        this.setLoadingState(false);
    };

    componentWillReceiveProps(nextProps) {
        nextProps.authenticated && this.getOrders();
    }

    render() {
        const orderRows = this.state.all_orders.map((order) =>
            <Order
                key={order.suborder_number}
                order_number={order.order_number}
                suborder_number={order.suborder_number}
                order_type={order.order_type}
                billing_name={order.customer.billing_name}
                date_received={order.date_received.slice(0, -9)}
                current_status={order.current_status}
                updateStatus={this.updateStatus}
                order={order}
                index={this.state.all_orders.indexOf(order)}
            />
        );

        return (
            <Container>
                {this.props.authenticated ? (
                    <Grid padded columns={3}>
                        <Segment basic className="-no-padding -no-margin">
                            <Header as="h1" className="-half">ePayments
                                <Container className="sub header">Department of Records</Container>
                            </Header>
                            <Segment basic className="-half -no-padding">
                                <div className="-float-right">
                                    Hi {this.props.user}
                                    <Button content='Logout' onClick={this.logOut} className="-margin-left"/>
                                </div>
                            </Segment>
                        </Segment>

                        <Dimmer inverted active={this.state.loading}>
                            <Loader content='Loading'/>
                        </Dimmer>
                        <Grid.Column width={3}>
                        </Grid.Column>
                        <Grid.Column width={11} className="-no-padding" id="orders-properties">
                            <Rail position="left" id="grid-column-search">
                                <OrderForm addOrder={this.addOrder}
                                           setLoadingState={this.setLoadingState}
                                           toggleCSV={this.toggleCSV}
                                           ref={orderForm => this.orderForm = orderForm}/>
                            </Rail>

                            <Header as="h1" dividing textAlign="center" className='-margin-top-none'>Order</Header>

                            <Rail position="right" id="rail-right">
                                <p><strong>Number of Items: {this.state.suborder_count}</strong></p>

                                <p><strong>Number of Orders: {this.state.order_count}</strong></p>

                                <Button.Group vertical size='medium'>
                                    <Button icon active={true}>
                                        <Icon name='print'/>
                                    </Button>
                                    {this.state.showCSVButton &&
                                    <Button content='Generate CSV' onClick={this.generateCSV}/>}
                                    <Button content='Order Sheets' onClick={this.printOrderSheet}/>
                                    <Button content='Big Labels' onClick={this.printBigLabels}/>
                                    <Button content='Small Labels' onClick={this.printSmallLabels}/>

                                    <Link to="/Order">
                                        <Button content='New Order'/>
                                    </Link>
                                </Button.Group>
                            </Rail>
                            <div id="grid-column-order" ref={elem => this.div = elem}>
                                {orderRows}
                                {this.state.suborder_count >= this.state.suborder_two && this.state.suborder_count !== 0 ? (
                                    <div className="center">
                                        <Button content="Load More"
                                                onClick={this.loadMore}/>
                                    </div>
                                ) : (<div className="center">
                                    {this.state.suborder_count === 0 ?
                                        (<p>No Results</p>) : (<p>End of Results</p>)}
                                </div>)
                                }
                            </div>
                        </Grid.Column>
                    </Grid>
                ) : (
                    <Segment id="center">
                        <Header as="h1" textAlign="center">ePayments
                            <Container className="sub header">Department of Records</Container>
                        </Header>
                        <LoginModal/>
                    </Segment>
                )}
            </Container>
        );
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Home);
