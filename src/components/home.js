import React from 'react';
import {Grid, Container, Header, Button, Segment, Divider, Dimmer, Loader} from 'semantic-ui-react';
import {connect} from 'react-redux';
import {mapDispatchToProps, mapStateToProps} from "../utils/reduxMappers";
import OrderForm from "./order_form";
import Order from "./order";
import LoginModal from "./login_modal"
import {csrfFetch} from "../utils/fetch"


class Home extends React.Component {
    constructor() {
        super();

        this.state = {
            all_orders: [],
            order_count: 0,
            suborder_count: 0,
            loading: true
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
            csrfFetch('api/v1.0/logout', {
                method: "DELETE",
            }).then((response) => (
                response.json()
            )).then((json) => {
                if (json.authenticated === false) {
                    this.props.logout();
                    alert("Logged Out");
                }
            });
        };
    };

    getOrders() {
        csrfFetch('api/v1.0/orders').then((response) => (
            response.json()
        )).then((json) => {
            this.addOrder(json.order_count, json.suborder_count, json.all_orders);
            this.setLoadingState(false)
        });
    };

    componentWillReceiveProps(nextProps) {
        nextProps.authenticated && this.getOrders();
    }


    render() {
        const orderRows = this.state.all_orders.map((order, index) =>
            <Order
                key={order.suborder_number}
                order_number={order.order_number}
                suborder_number={order.suborder_number}
                client_agency_name={order.client_agency_name}
                billing_name={order.billing_name}
                date_submitted={order.date_submitted.slice(0, -9)}
                current_status={order.current_status}
                updateStatus={this.updateStatus}
            />
        );

        return (
            <Container>
                {this.props.authenticated ? (
                    <Grid padded columns={3}>
                        <Grid.Column width={4}>
                            <Header as="h1" textAlign="center">ePayments
                                <Container className="sub header">Department of Records</Container>
                            </Header>
                            <Segment padded textAlign='center'>
                                <div>Hi {this.props.user}</div>
                                <br/>
                                <Button fluid content='Logout' onClick={this.logOut}/>
                            </Segment>
                            <OrderForm addOrder={this.addOrder} setLoadingState={this.setLoadingState} ref={orderForm => this.orderForm = orderForm}/>
                        </Grid.Column>
                        <Grid.Column width={1}/>
                        <Dimmer inverted active={this.state.loading}>
                            <Loader content='Loading'/>
                        </Dimmer>
                        <Grid.Column width={11} id="grid-column-order">
                            <Header as="h1" dividing textAlign="center">Order</Header>
                            <div>
                                <Button.Group size='medium' floated='right'>
                                    <Button labelPosition='left' icon='print'
                                            content='Order Sheets' onClick={this.printOrderSheet}/>
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
