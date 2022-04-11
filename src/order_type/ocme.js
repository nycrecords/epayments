import React from "react";
import "semantic-ui-css/semantic.min.css";

class OCME extends React.Component{

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
                    <div className="-fourth"> Borough: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["borough"]}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Date: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["date"]}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> First Name: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["first_name"]}
                    </div>
                </div>


                <div className="-row">
                    <div className="-fourth"> Middle Name: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["middle_name"] ? this.props.order_info["metadata"]["middle_name"] : ""}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Last Name: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["last_name"]}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Age: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["age"]  ? this.props.order_info["metadata"]["age"] : ""}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Certificate Number: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["certificate_number"] ? this.props.order_info["metadata"]["certificate_number"] : ""}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Number of Copies: </div>
                    <div className="-two-thirds"> {this.props.order_info["metadata"]["num_copies"]}</div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Raised Seal: </div>
                    <div className="-two-thirds"> {this.props.order_info["metadata"]["raised_seal"] ? "Yes" : "No"}</div>
                </div>

                {this.props.order_info["metadata"]["raised_seal"] &&
                    <div className="-row">
                        <div className="-fourth"> Raised Seal Copies: </div>
                        <div className="-two-thirds">
                            {this.props.order_info["metadata"]["raised_seal_copies"] ? this.props.order_info["metadata"]["raised_seal_copies"] : ""}
                        </div>
                    </div>
                }

                <div className="-row">
                    <div className="-fourth"> Delivery Method: </div>
                    <div className="-two-thirds"> {this.props.order_info["metadata"]["delivery_method"]} </div>
                </div>

                {this.props.order_info["metadata"]["contact_number"] &&
                    <div className="-row">
                        <div className="-fourth"> Contact Number: </div>
                        <div className="-two-thirds">
                            {this.props.order_info["metadata"]["contact_number"]}
                        </div>
                    </div>
                }

                {this.props.order_info["metadata"]["contact_email"] &&
                    <div className="-row">
                        <div className="-fourth"> Contact Email: </div>
                        <div className="-two-thirds">
                            {this.props.order_info["metadata"]["contact_email"]}
                        </div>
                    </div>
                }
            </div>
        )
    };
}


export default OCME;
