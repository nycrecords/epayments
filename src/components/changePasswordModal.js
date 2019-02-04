import React from 'react'
import {Button, Form, Header, Modal} from 'semantic-ui-react'
import {connect} from 'react-redux'
import {mapDispatchToProps, mapStateToProps} from "../utils/reduxMappers";
import {csrfFetch, handleFetchErrors} from "../utils/fetch"


class ChangePasswordModal extends React.Component {

    constructor() {
        super();

        this.state = {
            modalOpen: false,
            password: '',
            confirm_password: ''
        };

        this.handleOpen = (e) => this.setState({
            modalOpen: true,
        });

        this.handleClose = (e) => this.setState({
            modalOpen: false,
        });

        this.handleSubmit = (e) => {
            e.preventDefault();

            if (this.state.password !== this.state.confirm_password) {
                alert("Passwords do not match.")
            }
            else {
                csrfFetch('api/v1/password', {
                    method: 'PATCH',
                    body: JSON.stringify({
                        password: this.state.password,
                        confirm_password: this.state.confirm_password
                    })
                })
                    .then(handleFetchErrors)
                    .then((json) => {
                        alert(json.message)
                    })
                    .catch((error) => {
                        console.error(error)
                    });

                this.handleClose();
            }
        }
    }

    render() {
        return (
            <Modal trigger={<Button onClick={this.handleOpen}>Change Password</Button>}
                   open={this.state.modalOpen}
                   onClose={this.state.handleClose}>
                {this.props.authenticated && <Header>Change Password</Header>}
                <Modal.Content>
                    <Form>
                        <Form.Input label="New Password"
                                    minLength="6"
                                    maxLength="12"
                                    type="password"
                                    onChange={(e, {value}) => {
                                        this.setState({password: value})
                                    }}
                                    value={this.state.password}
                        />
                        <Form.Input label="Confirm Password"
                                    minLength="6"
                                    maxLength="12"
                                    type="password"
                                    onChange={(e, {value}) => {
                                        this.setState({confirm_password: value})
                                    }}
                                    value={this.state.confirm_password}
                        />
                        <Button type='submit' positive onClick={this.handleSubmit} floated='right'>Change
                            Password</Button>
                        <Button type='button' negative onClick={this.handleClose} floated='right'>Cancel</Button>
                        <br/>
                    </Form>
                    <br/>
                </Modal.Content>
            </Modal>
        )
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(ChangePasswordModal)
