/**
 * Created by walwong on 8/14/18.
 */
import React from "react";
import "semantic-ui-css/semantic.min.css";

class MarriageCert extends React.Component{

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
                    <div className="-fourth"> Groom Last Name: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["groom_last_name"] ? this.props.order_info["metadata"]["groom_last_name"] : ""}
                    </div>
                </div>
                    
                <div className="-row">
                    <div className="-fourth"> Groom First Name: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["groom_first_name"] ? this.props.order_info["metadata"]["groom_first_name"] : ""}
                    </div>
                </div>
                
                <div className="-row">
                    <div className="-fourth"> Bride Last Name: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["bride_last_name"] ? this.props.order_info["metadata"]["bride_last_name"] : ""}
                    </div>
                </div>
                
                <div className="-row">
                    <div className="-fourth"> Bride First Name: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["bride_first_name"] ? this.props.order_info["metadata"]["bride_first_name"] : ""}
                    </div>
                </div>
                
                <div className="-row">
                    <div className="-fourth"> Number of Copies: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["num_copies"] ? this.props.order_info["metadata"]["num_copies"] : ""}
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
                        {this.props.order_info["metadata"]["years"] ? this.props.order_info["metadata"]["years"] : ""}
                    </div>
                </div>
                    
                <div className="-row">
                    <div className="-fourth"> Marriage Place: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["marriage_place"] ? this.props.order_info["metadata"]["marriage_place"] : ""}
                    </div>
                </div>
                    
                <div className="-row">
                    <div className="-fourth"> Borough: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["metadata"]["borough"] ? this.props.order_info["metadata"]["borough"] : ""}
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


export default MarriageCert;
