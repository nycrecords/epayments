import React from 'react';
import {BrowserRouter as Router, Route} from "react-router-dom";
import Home from './home.js';
import NewOrderForm from "./newOrderForm";


//Renders the Page Layout
class App extends React.Component {
    render() {
        return (
            <Router>
                <div>
                    <Route exact path="/" component={Home}/>
                    <Route exact path="/Order" component={NewOrderForm}/>
                </div>
            </Router>
        )
    }
}

export default App