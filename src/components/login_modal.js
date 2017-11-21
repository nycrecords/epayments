import React from 'react'
import { Button, Header, Icon, Modal, Form} from 'semantic-ui-react'
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
            fetch('api/v1.0/login', {
                method: "POST",
                body: JSON.stringify({
                    email: this.state.email,
                    password: this.state.password
                })
            }).then((response) => (
                response.json()
            )).then((json) => {

            });

            this.handleClose();
        };
    }

    render() {
        return (
                <Modal trigger={<Button primary fluid onClick={this.handleOpen}>Login</Button>}
                       open={this.state.modalOpen}
                       onClose={this.state.handleClose}>
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

export default LoginModal
