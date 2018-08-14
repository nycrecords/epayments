/**
 * Created by walwong on 8/14/18.
 */
import React from 'react';
import 'semantic-ui-css/semantic.min.css';
import {csrfFetch} from "../utils/fetch"

class MarriageCert extends React.Component{
    constructor() {
        super();

        this.state = {
            modalOpen: false,
            order_type: '',
            customer_name: '',
            address:'',
            order_number: '',
            order_time: '',
            phone: '',
            email: '',
            suborder_number:'',
            certificate_number:'',
            groom_last_name:'',
            groom_first_name:'',
            bride_last_name:'',
            bride_first_name:'',
            num_of_copies:'',
            month:'',
            day:'',
            years:'',
            marriage_place:'',
            borough:'',
            letter:'',
            comment:'',
            order_info:''
        };

        this.add_data = (order_info) => {
            debugger;
            this.setState({
                order_type: order_info['order_type'],
                customer_name: order_info['customer']['billing_name'],
                address:order_info['customer']['address'],
                order_number: order_info['customer']['order_number'] ,
                order_time: order_info['order']['date_submitted'],
                phone: order_info['customer']['phone'],
                email: order_info['customer']['email'],
                suborder_number: order_info['suborder_number'],
                certificate_number: order_info['certificate_number'],
                groom_last_name: order_info['groom_last_name'],
                groom_first_name: order_info['groom_first_name'],
                bride_last_name: order_info["bride_last_name"],
                bride_first_name:order_info["bride_first_name"] ,
                num_of_copies:order_info["num_copies"] ,
                month: order_info["month"],
                day: order_info["day"] ,
                years: order_info["years"],
                marriage_place: order_info["marriage_place"] ? order_info["marriage_place"] : "",
                borough:order_info["borough"],
                letter:order_info['letter'] ? "yes" : 'no',
                comment:order_info['comment'],
            })
        };

        this.get_info = (suborder_number) => {
            csrfFetch('api/v1.0/more_info/'+ suborder_number, {
                method: "POST",
                body: JSON.stringify({
                    suborder_number: suborder_number,
                })
            })
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
                .then((json)=> {
                    this.add_data( json.order_info );
                }).catch((error =>{
                    console.error(error);
            }))
        }
    }

    render(){
        return(
            <p> {this.state.customer_name} <br/>
                {this.state.address}
            </p>
        )
    };
}

class MarriageSearch extends React.Component{
    constructor() {
        super();

        this.state = {
            modalOpen: false,
            order_type: '',
            customer_name: '',
            address:'',
            order_number: '',
            order_time: '',
            phone: '',
            email: '',
            suborder_number:'',
            groom_last_name:'',
            groom_first_name:'',
            bride_last_name:'',
            bride_first_name:'',
            num_of_copies:'',
            month:'',
            day:'',
            years:'',
            marriage_place:'',
            borough:'',
            letter:'',
            comment:'',
            order_info:''
        };

        this.add_data = (order_info) => {
            debugger;
            this.setState({
                order_type: order_info['order_type'],
                customer_name: order_info['customer']['billing_name'],
                address:order_info['customer']['address'],
                order_number: order_info['customer']['order_number'] ,
                order_time: order_info['order']['date_submitted'],
                phone: order_info['customer']['phone'],
                email: order_info['customer']['email'],
                suborder_number: order_info['suborder_number'],
                groom_last_name: order_info['groom_last_name'],
                groom_first_name: order_info['groom_first_name'],
                bride_last_name: order_info["bride_last_name"],
                bride_first_name:order_info["bride_first_name"] ,
                num_of_copies:order_info["num_copies"] ,
                month: order_info["month"],
                day: order_info["day"] ,
                years: order_info["years"],
                marriage_place: order_info["marriage_place"] ? order_info["marriage_place"] : "",
                borough:order_info["borough"],
                letter:order_info['letter'] ? "yes" : 'no',
                comment:order_info['comment'],
            })
        };

        this.get_info = () => {
            csrfFetch('api/v1.0/more_info/'+ this.props.suborder_number, {
                method: "POST",
                body: JSON.stringify({
                    suborder_number: this.props.suborder_number,
                })
            })
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
                .then((json)=> {
                    this.add_data( json.order_info );
                }).catch((error =>{
                    console.error(error);
            }))
        }
    }

    render(){
        return(
            <p> {this.state.customer_name} <br/>
                {this.state.address}
            </p>
        )
    };
}

export default {MarriageSearch, MarriageCert};