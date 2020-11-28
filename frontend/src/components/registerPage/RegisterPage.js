import React, {Component} from 'react';
import {Form, Button} from "react-bootstrap";
import PropTypes from 'prop-types';
import {registerUser} from '../../actions/auth'
import {createMessage} from "../../actions/messages";
import {Redirect} from "react-router-dom";
import { connect } from "react-redux";


class RegisterPage extends Component {
    state = {
        username: '',
        email: '',
        password: '',
        password2: '',
    };
    
    static propTypes = {
        registerUser: PropTypes.func.isRequired,
        isAuthenticated: PropTypes.bool
    };
    
    onSubmit = (e) => {
        e.preventDefault();
        const { username, email, password, password2 } = this.state;
        if (password !== password2) {
            this.props.createMessage({ passwordNotMatch: 'Passwords do not match'});
        } else {
            const newUser = {
                username, password, email
            };
            this.props.registerUser(newUser);
        }
    };
    
    onChange = (e) => this.setState({ [e.target.name]: e.target.value});


    render() {
        // TODO na środek to wpierdolić
        if (this.props.isAuthenticated) {
            return <Redirect to={"#/"} />;
        }
        
        const { username, password, email, password2} = this.state;
        return (
            <div className={"align-middle w-responsive"}>
                <Form onSubmit={this.onSubmit}>
                    <Form.Group controlId="formUsername">
                        <Form.Label>Nazwa użytkownika</Form.Label>
                        <Form.Control type="text" placeholder="Nazwa użytkownika" name={'username'} onChange={this.onChange} value={username}/>
                    </Form.Group>

                    <Form.Group controlId="formEmail">
                        <Form.Label>Adres e-mail</Form.Label>
                        <Form.Control type="email" placeholder="Wpisz email" name={"email"} onChange={this.onChange} value={email}/>
                        <Form.Text className="text-muted">
                            Nikomu nie udostępnimy Twojego adresu e-mail.
                        </Form.Text>
                    </Form.Group>

                    <Form.Group controlId="formPassword">
                        <Form.Label>Hasło</Form.Label>
                        <Form.Control type="password" placeholder="Wpisz hasło" name={"password"} onChange={this.onChange} value={password}/>
                    </Form.Group>

                    <Form.Group controlId="formCheckPassword">
                        <Form.Label>Powtórz hasło</Form.Label>
                        <Form.Control type="password" placeholder="Wpisz jeszcze raz hasło" name={"password2"} onChange={this.onChange} value={password2} />
                    </Form.Group>

                    <Button variant="success" type="submit">
                        Zarejestruj się
                    </Button>
                </Form>
            </div>
        );
    }
}

const mapStateToProps = (state) => ({
    isAuthenticated: state.auth.isAuthenticated,
});

export default connect(mapStateToProps, { registerUser, createMessage})(RegisterPage);