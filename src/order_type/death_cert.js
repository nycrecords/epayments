/**
 * Created by walwong on 8/15/18.
 */

import React from "react";
import "semantic-ui-css/semantic.min.css";

class DeathCert extends React.Component{

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
                        {this.props.order_info["metadata"]["certificate_number"] ? this.props.order_info["metadata"]["certificate_number"] : ""}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Last Name: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["last_name"]}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Middle Name: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["middle_name"] ? this.props.order_info["metadata"]["middle_name"] : ""}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> First Name: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["first_name"] ? this.props.order_info["metadata"]["first_name"] : ""}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Alt Last Name: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["alt_last_name"]  ? this.props.order_info["metadata"]["alt_last_name"] : ""}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Alt Middle Name: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["alt_middle_name"] ? this.props.order_info["metadata"]["alt_middle_name"] : ""}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Alt First Name: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["alt_first_name"] ? this.props.order_info["metadata"]["alt_first_name"] : ""}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Age at Death: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["age_at_death"] ? this.props.order_info["metadata"]["age_at_death"]: ""}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Month: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["month"] ? this.props.order_info["metadata"]["month"] : ""}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Day: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["day"] ? this.props.order_info["metadata"]["day"] : ""}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Years: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["years"]}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Death Place: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["death_place"] ? this.props.order_info["metadata"]["death_place"]  : ""}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Borough: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["borough"]}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Father Name: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["father_name"] ? this.props.order_info["metadata"]["father_name"] : ""}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Mother Name: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["mother_name"] ? this.props.order_info["metadata"]["mother_name"] : ""}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Number of Copies: </div>
                    <div className="-two-thirds"> {this.props.order_info["metadata"]["num_copies"]}</div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Exemplification:</div>
                    <div
                        className="-two-thirds"> {this.props.order_info["metadata"]["exemplification"] ? "Yes" : "No"}</div>
                </div>

                {this.props.order_info["metadata"]["exemplification"] &&
                <div className="-row">
                    <div className="-fourth"> Exemplification Copies:</div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["exemplification_copies"] ? this.props.order_info["metadata"]["exemplification_copies"] : ""}
                    </div>
                </div>
                }

                <div className="-row">
                    <div className="-fourth"> Raised Seal:</div>
                    <div
                        className="-two-thirds"> {this.props.order_info["metadata"]["raised_seal"] ? "Yes" : "No"}</div>
                </div>

                {this.props.order_info["metadata"]["raised_seal"] &&
                <div className="-row">
                    <div className="-fourth"> Raised Seal Copies:</div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["raised_seal_copies"] ? this.props.order_info["metadata"]["raised_seal_copies"] : ""}
                    </div>
                </div>
                }

                <div className="-row">
                    <div className="-fourth"> No Amends:</div>
                    <div className="-two-thirds"> {this.props.order_info["metadata"]["no_amends"] ? "Yes" : "No"}</div>
                </div>

                {this.props.order_info["metadata"]["no_amends"] &&
                <div className="-row">
                    <div className="-fourth"> No Amends Copies:</div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["no_amends_copies"] ? this.props.order_info["metadata"]["no_amends_copies"] : ""}
                    </div>
                </div>
                }

                <div className="-row">
                    <div className="-fourth"> Delivery Method: </div>
                    <div className="-two-thirds"> {this.props.order_info["metadata"]["delivery_method"]} </div>
                </div>
            </div>
        )
    };
}


export default DeathCert;
