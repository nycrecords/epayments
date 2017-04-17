/**
 * Created by sinsang on 4/17/17.
 */

import React from 'react'

export default class Header extends React.Component {
    render() {
        return (
            <header className='top'>
                <h1>ePayments</h1>
                <h3 className='tagline'><span>{this.props.tagline}</span></h3>
            </header>
        )
    };
}

Header.propTypes = {
    tagline: React.PropTypes.string.isRequired
};
