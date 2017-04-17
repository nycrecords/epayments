/**
 * Created by sinsang on 4/17/17.
 */

import React from 'react'

export default class Inventory extends React.Component {

    render() {
        return (
            <div>
                <Header tagline={this.props.tagline}/>
                <br />
                <OrderForm {...this.props} />
            </div>
        )
    }
}

Inventory.propTypes = {
    tagline: React.PropTypes.string.isRequired
};
