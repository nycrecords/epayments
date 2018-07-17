import React from 'react';
import ReactDOM from 'react-dom';
import 'semantic-ui-css/semantic.min.css';
import './css/index.css';
import {Provider} from 'react-redux';
import store  from './store/index'
import App from './components/app.js';
import { render } from 'react-dom'
import { BrowserRouter } from 'react-router-dom'


ReactDOM.render(
    <Provider store={store}>
        <BrowserRouter>
            <App />
        </BrowserRouter>
    </Provider>,
    document.getElementById('root')
);
