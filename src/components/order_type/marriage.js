/**
 * Created by walwong on 8/14/18.
 */
import React from 'react';
import {Button, Header, Modal, Form, TextArea} from 'semantic-ui-react';
import 'semantic-ui-css/semantic.min.css';
import {csrfFetch} from "../utils/fetch"

class MarriageCert extends React.Component{
    constructor() {
        super();

        this.state = {
            modalOpen: false,
            order_type: '',
            customer_name: '',
            order_number: '',
            order_time: '',
            phone: '',
            email: ''

        };

        this.add_data = (order_info) => {
            debugger;
            this.setState({
                order_type: order_info['order_type'],
                customer_name: order_info['customer']['billing_name'],
                order_type_info: order_info['order_type']
            })
        };

        this.get_info = (suborder_number) => {
            csrfFetch('api/v1.0/more_info/'+this.props.suborder_number, {
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
                    this.add_data(json.order_info, json.suborder_info);
                }).catch((error =>{
                    console.error(error);
            }))
        }
    }
}

class MarriageSearch extends React.Component{

}

export default MarriageSearch;
export default MarriageCert;