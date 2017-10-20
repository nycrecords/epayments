import React from 'react';
import {Accordion, Menu, Dropdown, Icon} from 'semantic-ui-react';
import 'semantic-ui-css/semantic.min.css';


class History extends React.Component {


    handleClick = (e) => {
        this.props.handleHistoryRequest(this.props.suborder_no)
    };
    render(){
        return(
            <Accordion>
                <Accordion.Title onClick={this.handleClick}>
                  <Icon name='dropdown' />
                  History
                </Accordion.Title>
                <Accordion.Content>
                  <p>
                    The history goes here
                  </p>
                </Accordion.Content>
            </Accordion>
        )
    }
}

export default History;