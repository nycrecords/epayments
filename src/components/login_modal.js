import React from 'react'
import {Button, Form, Header, Modal} from 'semantic-ui-react'
import {connect} from 'react-redux'
import {mapDispatchToProps, mapStateToProps} from "../utils/reduxMappers";
import {csrfFetch} from "../utils/fetch"


class LoginModal extends React.Component {

    constructor() {
        super();

        this.state = {
            modalOpen: false,
            email: '',
            password: ''
        };

        this.handleOpen = (e) => this.setState({
            modalOpen: true,
        });

        this.handleClose = (e) => this.setState({
            modalOpen: false,
        });

        this.handleSubmit = (e) => {
            e.preventDefault();
            csrfFetch('api/v1/login', {
                method: 'post',
                body: JSON.stringify({
                    email: this.state.email,
                    password: this.state.password
                })
            }).then((response) => (
                response.json()
            )).then((json) => {
                if (json.authenticated) {
                    this.props.login(json.email);
                }
                else {
                    alert(json.message);
                }
            });
            this.handleClose();
        };
    }

    render() {
        return (
            <Modal trigger={<Button primary fluid onClick={this.handleOpen}>Log In</Button>}
                   open={this.state.modalOpen}
                   onClose={this.state.handleClose}>
                {this.props.authenticated && <Header>Logged In</Header>}
                <Header icon='user' content='Enter your Credentials'/>
                <Modal.Content>
                    <Form>
                        <Form.Input label="Email" placeholder="Email" maxLength="64"
                                    onChange={(e, {value}) => {
                                        this.setState({email: value})
                                    }}
                                    value={this.state.email}
                        />
                        <Form.Input label="Password" placeholder="Password" maxLength="64"
                                    type='password'
                                    onChange={(e, {value}) => {
                                        this.setState({password: value})
                                    }}
                                    value={this.state.password}
                        />
                        <Button type='submit' positive onClick={this.handleSubmit} floated='right'>Log In</Button>
                        <Button type='button' negative onClick={this.handleClose} floated='right'>Cancel</Button>
                        <br/>
                    </Form>
                    <br/>
                </Modal.Content>
            </Modal>
        )
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(LoginModal)
