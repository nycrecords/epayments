/**
 * Created by walwong on 8/15/18.
 */

import React from "react";
import "semantic-ui-css/semantic.min.css";

class PhotoGallery extends React.Component{

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
                    <div className="-fourth"> Image ID: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["image_id"] ? this.props.order_info["metadata"]["image_id"] : "n/a"}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Description: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["description"] ? this.props.order_info["metadata"]["description"]: "n/a"}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Additional Description: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["additional_description"] ? this.props.order_info["metadata"]["additional_description"]: "n/a"}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Size: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["size"] ? this.props.order_info["metadata"]["size"]: "n/a"}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Number of Copies: </div>
                    <div className="-two-thirds"> {this.props.order_info["metadata"]["num_copies"]}</div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Mail Pickup: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["mail"] ? "Mail" : "Pickup"}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Contact Number: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["contact_number"] ? this.props.order_info["metadata"]["contact_number"] : "n/a"}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Personal Use Agreement: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["personal_use_agreement"] ? "True" : "False" }
                    </div>
                </div>
                <br />

                <div className="-row">
                    <div className="-fourth"> Comment: </div>
                    <div className="-two-thirds"> {this.props.order_info["metadata"]["comment"]} </div>
                </div>

            </div>
        )
    };
}


export default PhotoGallery;
