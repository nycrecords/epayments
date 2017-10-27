import React from 'react';
import {Accordion, Label, Icon, Table} from 'semantic-ui-react';
import 'semantic-ui-css/semantic.min.css';
import HistoryRow from './historyRow'

class History extends React.Component {

    constructor() {
        super();

        this.state = {
            all_history: []
        };

        this.handleClick = (e) => {
            fetch('api/v1.0/history/' + this.props.suborder_no).then((response) => (
                response.json()
            )).then((json) => {
                this.setState({all_history: json.history});
            });
        };
    }

    render() {
         const HistoryRows = this.state.all_history.map((history, index) =>
            <HistoryRow
                comment={history.comment}
                previous_value={history.previous_value}
                current_status={history.current_status}
                timestamp={history.timestamp}
            />

         );

        return(
            <Accordion>
                <Accordion.Title onClick={this.handleClick }>
                  <Icon name='dropdown' />
                    <Label color='blue' content={'History'}/>
                </Accordion.Title>
                <Accordion.Content>
                  <p>
                    <Table called selectable>
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

                  </p>
                </Accordion.Content>
            </Accordion>
        )
    }
}

export default History;