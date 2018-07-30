import React from 'react';
import {Button, Container, Dimmer, Divider, Grid, Header, Icon, Loader, Segment} from 'semantic-ui-react';
import {connect} from 'react-redux';
import {mapDispatchToProps, mapStateToProps} from "../utils/reduxMappers";
import OrderForm from "./order_form";
import Order from "./order";
import LoginModal from "./login_modal";
import {csrfFetch, handleFetchErrors} from "../utils/fetch"


class Home extends React.Component {
    constructor() {
        super();

        this.state = {
            all_orders: [],
            order_count: 0,
            suborder_count: 0,
            loading: true,
            showCSVButton: false
        };

        this.addOrder = (order_count, suborder_count, orders) => {
            this.setState({
                all_orders: orders,
                order_count: order_count,
                suborder_count: suborder_count
            });
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
                this.addOrder(json.order_count, json.suborder_count, json.all_orders);
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
                key={order._source.suborder_number}
                order_number={order._source.order_number}
                suborder_number={order._source.suborder_number}
                order_type={order._source.order_type}
                billing_name={order._source.billing_name}
                date_received={order._source.date_received.slice(0, -9)}
                current_status={order._source.current_status}
                updateStatus={this.updateStatus}
            />
        );

        return (
            <Container>
                {this.props.authenticated ? (
                    <Grid padded columns={3}>
                        <Grid.Column width={4} id="grid-column-search">
                            <Header as="h1" textAlign="center">ePayments
                                <Container className="sub header">Department of Records</Container>
                            </Header>
                            <Segment padded textAlign='center'>
                                <div>Hi {this.props.user}</div>
                                <br/>
                                <Button fluid content='Logout' onClick={this.logOut}/>
                            </Segment>
                            <OrderForm addOrder={this.addOrder} setLoadingState={this.setLoadingState}
                                       toggleCSV={this.toggleCSV} ref={orderForm => this.orderForm = orderForm}/>
                        </Grid.Column>
                        <Grid.Column width={1}/>
                        <Dimmer inverted active={this.state.loading}>
                            <Loader content='Loading'/>
                        </Dimmer>
                        <Grid.Column width={11} id="grid-column-order">
                            <Header as="h1" dividing textAlign="center">Order</Header>
                            <div>
                                <Button.Group size='medium' floated='right'>
                                    <Button icon active={true}>
                                        <Icon name='print'/>
                                    </Button>
                                    {this.state.showCSVButton &&
                                    <Button content='Generate CSV' onClick={this.generateCSV}/>}
                                    <Button content='Order Sheets' onClick={this.printOrderSheet}/>
                                    <Button content='Big Labels' onClick={this.printBigLabels}/>
                                    <Button content='Small Labels' onClick={this.printSmallLabels}/>
                                </Button.Group>
                                <strong>Number of Items: {this.state.suborder_count}</strong>
                                <br/>
                                <strong>Number of Orders: {this.state.order_count}</strong>
                            </div>
                            <div>
                                <Divider clearing/>
                            </div>
                            {orderRows}
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
        )
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Home);
