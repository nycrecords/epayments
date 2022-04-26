import React from "react";
import "semantic-ui-css/semantic.min.css";

class HVR extends React.Component {
    render() {
        return (
            <div className="-order-modals">
                {this.props.order_info["customer"]["billing_name"]} <br/>
                {this.props.order_info["customer"]["address"]} <br/>
                <h2>{this.props.order_info["order_type"]}</h2>
                <strong>Order number:</strong> {this.props.order_info["order_number"]}<br/>
                <strong>Order time:</strong> {this.props.order_info["date_submitted"]} <br/>
                <strong>Phone:</strong> {this.props.order_info["customer"]["phone"]} <br/>
                <strong>E-mail:</strong> {this.props.order_info["customer"]["email"]} <br/>
                <strong>Suborder Number</strong> {this.props.order_info["suborder_number"]} <br/> <br/>

                <div className="-row">
                    <div className="-fourth"> Link:</div>
                    <div className="-two-thirds"><a
                        href={this.props.order_info["metadata"]["link"]}
                        target="_blank">{this.props.order_info["metadata"]["link"]}</a>
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Record ID:</div>
                    <div className="-two-thirds"> {this.props.order_info["metadata"]["record_id"]}</div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Type:</div>
                    <div className="-two-thirds"> {this.props.order_info["metadata"]["type"]}</div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Number of Copies:</div>
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
                    <div className="-fourth"> Delivery Method:</div>
                    <div className="-two-thirds"> {this.props.order_info["metadata"]["delivery_method"]} </div>
                </div>
            </div>
        )
    };
}

export default HVR;