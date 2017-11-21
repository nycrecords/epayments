import React from 'react';
import {Accordion, Label, Icon, Table} from 'semantic-ui-react';
import 'semantic-ui-css/semantic.min.css';
import HistoryRow from './historyRow'
import '../css/history_acord.css'

class History extends React.Component {

    constructor() {
        super();

        this.state = {
            all_history: [],
            activeIndex: false
        };


        this.handleClick = (e) => {
            if (this.state.activeIndex === false){
                this.setState({activeIndex: true});
                fetch('api/v1.0/history/' + this.props.suborder_number).then((response) => (
                    response.json()
                )).then((json) => {
                    this.setState({all_history: json.history});
                });
            }
        }
    };

    render() {
         const HistoryRows = this.state.all_history.map((history, index) =>
            <HistoryRow
                key={history.id}
                comment={history.comment}
                previous_value={history.previous_status}
                current_status={history.new_status}
                timestamp={history.timestamp}
            />

         );

        return(
            <Accordion onTitleClick={this.handleClick}>
                <Accordion.Title>
                  <Icon name='dropdown' />
                    <Label color='blue' content={'History'}/>
                </Accordion.Title>
                <Accordion.Content>
                    <Table celled selectable>
                        <Table.Header>
                            <Table.Row>
                                <Table.HeaderCell>Date/Time</Table.HeaderCell>
                                <Table.HeaderCell>Previous Status</Table.HeaderCell>
                                <Table.HeaderCell>Updated Status</Table.HeaderCell>
                                <Table.HeaderCell>Comment</Table.HeaderCell>
                            </Table.Row>
                        </Table.Header>

                        <Table.Body>
                            {HistoryRows}
                        </Table.Body>

                    </Table>

                </Accordion.Content>
            </Accordion>
        )
    }
}

export default History;