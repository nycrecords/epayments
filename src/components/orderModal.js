/**
 * Created by walwong on 8/13/18.
 */
import React from 'react';
import {Button, Modal} from 'semantic-ui-react';
import 'semantic-ui-css/semantic.min.css';
import MarriageCert from '../order_type/marriage_cert'
import MarriageSearch from '../order_type/marriage_search'
import BirthCert from '../order_type/birth_cert'
import BirthSearch from '../order_type/birth_search'
import DeathCert from '../order_type/death_cert'
import DeathSearch from '../order_type/death_search'
import TaxPhoto from '../order_type/tax_photo'
import PhotoGallery from '../order_type/photo_gallery'
import PropertyCard from '../order_type/property_card'
import OCME from '../order_type/ocme'
import {csrfFetch} from "../utils/fetch"

class OrderModal extends React.Component {
    constructor() {
        super();

        this.state = {
            modalOpen: false,
            order_info:''
        };

        this.add_data = (order_info) =>{
            this.setState({
                order_info: order_info
            })
        };

        this.handleOpen = () => {
            csrfFetch('api/v1/more_info/'+ this.props.suborder_number, {
                method: "POST",
                body: JSON.stringify({
                    suborder_number: this.props.suborder_number,
                })
            })
                .then(response => {
                // check response status to logout user if backend session expired
                    switch (response.status) {
                        case 500:
                            throw Error(response.statusText);
                        case 401:
                            this.props.authenticated && this.props.logout();
                            throw Error(response.statusText);
                        case 200:
                            return response.json();
                        default:
                            throw Error("Unhandled HTTP status code");
                    }
                })
                .then((json)=> {
                    this.add_data( json.order_info );
                    this.setState({
                        modalOpen: true
                    });
                }).catch((error =>{
                    console.error(error);
            }))

        };

        this.handleClose = (e) =>
            this.setState({
            modalOpen: false,
            });
    }

    render() {
        let orderInfo;
        switch (this.props.order_type){
            case 'Marriage Cert':
                orderInfo=(
                    <MarriageCert order_info={this.state.order_info}/>
                );
                break;
            case 'Marriage Search':
                orderInfo=(
                    <MarriageSearch order_info={this.state.order_info}/>
                );
                break;
            case 'Birth Cert':
                orderInfo=(
                    <BirthCert order_info={this.state.order_info}/>
                );
                break;
            case 'Birth Search':
                orderInfo=(
                    <BirthSearch order_info={this.state.order_info}/>
                );
                break;
            case 'Death Cert':
                orderInfo=(
                    <DeathCert order_info={this.state.order_info}/>
                );
                break;
            case 'Death Search':
                orderInfo=(
                    <DeathSearch order_info={this.state.order_info}/>
                );
                break;
            case 'Tax Photo':
                orderInfo=(
                    <TaxPhoto order_info={this.state.order_info}/>
                );
                break;
            case 'Property Card':
                orderInfo=(
                    <PropertyCard order_info={this.state.order_info}/>
                );
                break;
            case 'Photo Gallery':
                orderInfo=(
                    <PhotoGallery order_info={this.state.order_info}/>
                );
                break;
            case 'OCME':
                orderInfo=(
                    <OCME order_info={this.state.order_info}/>
                );
                break;
            default:
                orderInfo=(<p> That's not supposed to happen, Let the I.T. folks know</p>);
                break;
        }

        return (
            <Modal
                trigger={<Button onClick={this.handleOpen} compact size='small' floated='right'>More Info</Button>}
                open={this.state.modalOpen}
                onClose={this.state.handleClose}
                id="orderModal">

                {orderInfo}

                <Modal.Actions>
                    <Button negative onClick={this.handleClose}>Close</Button>
                </Modal.Actions>
            </Modal>
        )
    }
}

export default OrderModal