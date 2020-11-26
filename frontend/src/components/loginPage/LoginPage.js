import React, {Component} from 'react';
import {Form, Button} from "react-bootstrap";
import {Redirect} from "react-router-dom";
import {PropTypes} from "prop-types";

class LoginPage extends Component {
    state = {
        username: "",
        password: "",
    };

    static propTypes = {
        login: PropTypes.func.isRequired,
        isAuthenticated: PropTypes.bool
    };

    onSubmit = (e) => {
        e.preventDefault();
        this.props.login(this.state.username, this.state.password);
    };

    onChange = (e) => this.setState({ [e.target.name] : e.target.value});

    render() {
        if(this.props.isAuthenticated) return <Redirect to={'/#'} />
        // TODO na środek to wpierdolić
        const { username, password } = this.state;
        return (
            <div className={"align-middle w-responsive"}>
                <Form onSubmit={this.onSubmit}>
                    <Form.Group controlId="formUsername">
                        <Form.Label>Nazwa użytkownika</Form.Label>
                        <Form.Control type="email" placeholder="Nazwa użytkownika" name={'username'} onChange={this.onChange} value={username}/>
                    </Form.Group>

                    <Form.Group controlId="formPassword">
                        <Form.Label>Hasło</Form.Label>
                        <Form.Control type="password" placeholder="Wpisz hasło" name={'password'} onChange={this.onChange} value={password}/>
                    </Form.Group>

                    <Button variant="success" type="submit">
                        Zaloguj się
                    </Button>
                </Form>
            </div>
        );
    }
}

export default LoginPage;