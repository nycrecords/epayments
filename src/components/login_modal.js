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
                        <Form.Field>
                          <label>Email</label>
                          <input placeholder='Email' />
                        </Form.Field>
                        <Form.Field>
                          <label>Password</label>
                          <input type='password' placeholder='Password' />
                        </Form.Field>
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
