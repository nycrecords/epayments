/**
 * Created by walwong on 8/15/18.
 */

import React from "react";
import "semantic-ui-css/semantic.min.css";

class BirthCert extends React.Component{

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
                    <div className="-fourth"> Certificate Number: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["certificate_number"] ? this.props.order_info["metadata"]["certificate_number"] : "n/a"}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Gender: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["gender"] ? this.props.order_info["metadata"]["gender"] : "n/a"}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Last Name: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["last_name"]  ? this.props.order_info["metadata"]["last_name"] : "n/a"}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Middle Name: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["middle_name"] ? this.props.order_info["metadata"]["middle_name"] : "n/a"}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> First Name: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["first_name"] ? this.props.order_info["metadata"]["first_name"] : "n/a"}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Father Name: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["father_name"] ? this.props.order_info["metadata"]["father_name"] : "n/a"}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Mother Name: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["mother_name"] ? this.props.order_info["metadata"]["mother_name"] : "n/a"}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Number of Copies: </div>
                    <div className="-two-thirds"> {this.props.order_info["metadata"]["num_copies"]}</div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Month: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["month"] ? this.props.order_info["metadata"]["month"] : "n/a"}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Day: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["day"] ? this.props.order_info["metadata"]["day"] : "n/a"}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Years: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["years"] ? this.props.order_info["metadata"]["years"] : "n/a"}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Birth Place: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["birth_place"] ? this.props.order_info["metadata"]["birth_place"]  : "n/a"}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Borough: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["borough"] ? this.props.order_info["metadata"]["borough"] : "n/a"}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Letter: </div>
                    <div className="-two-thirds"> {this.props.order_info["metadata"]["letter"] ? "Yes" : "No"} </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Comment: </div>
                    <div className="-two-thirds"> {this.props.order_info["metadata"]["comment"]} </div>
                </div>
            </div>
        )
    };
}


export default BirthCert;
