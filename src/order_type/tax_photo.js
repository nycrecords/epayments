/**
 * Created by walwong on 8/15/18.
 */

import React from "react";
import "semantic-ui-css/semantic.min.css";

class TaxPhoto extends React.Component{

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
                    <div className="-fourth"> Collection: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["collection"] ? this.props.order_info["metadata"]["collection"] : ""}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Borough: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["borough"]  ? this.props.order_info["metadata"]["borough"] : ""}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Roll: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["roll"] ? this.props.order_info["metadata"]["roll"] : ""}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Block: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["block"] ? this.props.order_info["metadata"]["block"] : ""}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Lot: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["lot"] ? this.props.order_info["metadata"]["lot"]: ""}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Building Number: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["building_number"] ? this.props.order_info["metadata"]["building_number"]: ""}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Street: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["street"] ? this.props.order_info["metadata"]["street"]: ""}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Description: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["description"] ? this.props.order_info["metadata"]["description"]: ""}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Size: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["size"] ? this.props.order_info["metadata"]["size"]: ""}
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
                        {this.props.order_info["metadata"]["contact_number"] ? this.props.order_info["metadata"]["contact_number"] : ""}
                    </div>
                </div>
            </div>
        )
    };
}


export default TaxPhoto;
