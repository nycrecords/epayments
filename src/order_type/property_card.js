/**
 * Created by walwong on 8/15/18.
 */

import React from 'react';
import 'semantic-ui-css/semantic.min.css';

class PropertyCard extends React.Component{

    render(){
        return(
            <div className="-order-modals">
                {this.props.order_info['customer']['billing_name']} <br/>
                {this.props.order_info['customer']['address']}  <br/>
                <h2>{this.props.order_info['order_type']}</h2>
                <strong>Order number:</strong> {this.props.order_info['customer']['order_number']}<br/>
                <strong>Order time:</strong> {this.props.order_info['date_submitted']} <br/>
                <strong>Phone:</strong> {this.props.order_info['customer']['phone']} <br/>
                <strong>E-mail:</strong> {this.props.order_info['customer']['email']} <br/>
                <strong>Suborder Number</strong> {this.props.order_info['suborder_number']} <br/> <br/>

                <div className="-row">
                    <div className="-fourth"> Borough: </div>
                    <div className="-two-thirds">
                        {this.props.order_info['borough']  ? this.props.order_info['borough'] : "n/a"}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Block: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["block"] ? this.props.order_info["block"] : "n/a"}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Lot: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["lot"] ? this.props.order_info["lot"]: "n/a"}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Building Number: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["building_number"] ? this.props.order_info["building_number"]: "n/a"}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Street: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["street"] ? this.props.order_info["street"]: "n/a"}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Description: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["description"] ? this.props.order_info["description"]: "n/a"}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Certified: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["mail"] ? 'Certified' : "Not Certified"}
                    </div>
                </div>

                <div className="-row">
                    <div className="-fourth"> Mail Pickup: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["mail"] ? 'Mail' : "Pickup"}
                    </div>
                </div>
            </div>
        )
    };
}


export default PropertyCard;
