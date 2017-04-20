import React from 'react'
import {Grid, Container} from 'semantic-ui-react'
// import './index.css';


class App extends React.Component {
    render() {
        return (
            <Grid divided="vertically">
                <Grid.Row columns={2}>
                    <Grid.Column>
                        <Container text>
                            <p>This should be on the left column.</p>
                        </Container>
                    </Grid.Column>
                    <div class="page-divider">dasd</div>
                    <Grid.Column>
                        <Container text>
                            <h1>This should be on the right column</h1>
                        </Container>
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        );
    }
}


export default App
