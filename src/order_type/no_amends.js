import React from "react";
import {Button} from 'semantic-ui-react'
import "semantic-ui-css/semantic.min.css";

class NoAmends extends React.Component{
    constructor() {
        super();

        this.downloadFile = () => {
            window.open("/api/v1/uploads/" + this.props.suborder_number, "_blank")
        }
    }

    render(){
        return(
            <div className="-order-modals">
                {this.props.order_info["customer"]["billing_name"]} <br/>
                {this.props.order_info["customer"]["address"]}  <br/>
                <h2>{this.props.order_info["order_type"]}</h2>
                <strong>Order number:</strong> {this.props.order_info["order_number"]}<br/>
                <strong>Order time:</strong> {this.props.order_info["date_submitted"]} <br/>
                <strong>Phone:</strong> {this.props.order_info["customer"]["phone"]} <br/>
                <strong>E-mail:</strong> {this.props.order_info["customer"]["email"]} <br/>
                <strong>Suborder Number</strong> {this.props.order_info["suborder_number"]} <br/> <br/>

                <div className="-row">
                    <div className="-fourth"> Number of Copies: </div>
                    <div className="-two-thirds"> {this.props.order_info["metadata"]["num_copies"]}</div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Filename: </div>
                    <div className="-two-thirds"> {this.props.order_info["metadata"]["filename"]}</div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Delivery Method: </div>
                    <div className="-two-thirds"> {this.props.order_info["metadata"]["delivery_method"]} </div>
                </div>

                <br />
                <Button primary onClick={this.downloadFile}>Download File</Button>
            </div>
        )
    };
}

export default NoAmends;
