import React from 'react';
import {Table} from 'semantic-ui-react';
import 'semantic-ui-css/semantic.min.css';

class HistoryRow extends React.Component {
    render() {
        return (
                <Table.Row>
                    <Table.Cell>{this.props.timestamp}</Table.Cell>
                    <Table.Cell>{this.props.previous_value}</Table.Cell>
                    <Table.Cell>{this.props.current_status}</Table.Cell>
                    <Table.Cell>{this.props.comment}</Table.Cell>
                </Table.Row>
        )
    }
}

export default HistoryRow