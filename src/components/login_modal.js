import React from 'react'
import {Button, Header, Modal, Form} from 'semantic-ui-react'
import {connect} from 'react-redux'
import {mapStateToProps, mapDispatchToProps} from "../utils/reduxMappers";
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
            csrfFetch('api/v1.0/login', {
                method: 'post',
                body: JSON.stringify({
                    email: this.state.email,
                    password: this.state.password
                })
            }).then((response) => (
                response.json()
            )).then((json) => {
                // if (json.authenticated === true) {
                //     this.props.login(json.email);
                //     alert("Hi "+ json.email);
                // }
                json.authenticated ? this.props.login(json.email) : alert(json.message);
            });

            this.handleClose();
        };
    }

    render() {
        return (
                <Modal trigger={<Button primary fluid onClick={this.handleOpen}>Login</Button>}
                       open={this.state.modalOpen}
                       onClose={this.state.handleClose}>
                    {this.props.authenticated && <Header>Logged In</Header>}
                  <Header icon='user' content='Enter your Credentials' />
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
                          <Button type='submit' positive onClick={this.handleSubmit} floated='right'>Submit</Button>
                          <Button negative onClick={this.handleClose} floated='right'>Cancel</Button>
                          <br/>
                      </Form>
                      <br/>
                  </Modal.Content>
                </Modal>
        )
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(LoginModal)
