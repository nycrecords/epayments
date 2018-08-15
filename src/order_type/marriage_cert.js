/**
 * Created by walwong on 8/14/18.
 */
import React from 'react';
import 'semantic-ui-css/semantic.min.css';

class MarriageCert extends React.Component{

    render(){
        return(
            <div className="-order-modals">
                {this.props.order_info['customer']['billing_name']} <br/>
                {this.props.order_info['customer']['address']}  <br/>
                <h2>{this.props.order_info['order_type']}</h2>
                <strong>Order number:</strong> {this.props.order_info['customer']['order_number']}<br/>
                <strong>Order time:</strong> {this.props.order_info['order']['date_submitted']} <br/>
                <strong>Phone:</strong> {this.props.order_info['customer']['phone']} <br/>
                <strong>E-mail:</strong> {this.props.order_info['customer']['email']} <br/>
                <strong>Suborder Number</strong> {this.props.order_info['suborder_number']} <br/> <br/>

                <div className="-row">
                    <div className="-fourth"> Certificate Number: </div>
                    <div className="-two-thirds">
                        {this.props.order_info['certificate_number'] ? this.props.order_info['certificate_number'] : "N/A"}
                    </div>
                </div>
                    
                <div className="-row">
                    <div className="-fourth"> Groom Last Name: </div>
                    <div className="-two-thirds">
                        {this.props.order_info['groom_last_name'] ? this.props.order_info['groom_last_name'] : "NA"}
                    </div>
                </div>
                    
                <div className="-row">
                    <div className="-fourth"> Groom First Name: </div>
                    <div className="-two-thirds">
                        {this.props.order_info['groom_first_name'] ? this.props.order_info['groom_first_name'] : "NA"}
                    </div>
                </div>
                
                <div className="-row">
                    <div className="-fourth"> Bride Last Name: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["bride_last_name"] ? this.props.order_info["bride_last_name"] : "NA"}
                    </div>
                </div>
                
                <div className="-row">
                    <div className="-fourth"> Bride First Name: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["bride_first_name"] ? this.props.order_info["bride_first_name"] : "NA"}
                    </div>
                </div>
                
                <div className="-row">
                    <div className="-fourth"> Number of Copies: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["num_copies"] ? this.props.order_info["num_copies"] : "NA"}
                    </div>
                </div>
                
                <div className="-row">
                    <div className="-fourth"> Month: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["month"] ? this.props.order_info["month"] : "NA"}
                    </div>
                </div>
                
                <div className="-row">
                    <div className="-fourth"> Day: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["day"] ? this.props.order_info["day"] : "NA"}
                    </div>
                </div>
                
                <div className="-row">
                    <div className="-fourth"> Years: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["years"] ? this.props.order_info["years"] : "NA"}
                    </div>
                </div>
                    
                <div className="-row">
                    <div className="-fourth"> Marriage Place: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["marriage_place"] ? this.props.order_info["marriage_place"] : "N/A"}
                    </div>
                </div>
                    
                <div className="-row">
                    <div className="-fourth"> Borough: </div>
                    <div className="-two-thirds">
                        {this.props.order_info["borough"] ? this.props.order_info["borough"] : "NA"}
                    </div>
                </div>
                    
                <div className="-row">
                    <div className="-fourth"> Letter: </div>
                    <div className="-two-thirds"> {this.props.order_info['letter'] ? "Yes" : 'No'} </div>
                </div>
                
                <div className="-row">
                    <div className="-fourth"> Comment: </div>
                    <div className="-two-thirds"> {this.props.order_info['comment']} </div>
                </div>            
            </div>
        )
    };
}


export default MarriageCert;
