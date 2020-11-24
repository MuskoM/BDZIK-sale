import React, {Component} from 'react';
import {Form, Button} from "react-bootstrap";

class LoginPage extends Component {


    render() {
        // TODO na środek to wpierdolić
        return (
            <div className={"align-middle w-responsive"}>
                <Form>
                    <Form.Group controlId="formUsername">
                        <Form.Label>Nazwa użytkownika</Form.Label>
                        <Form.Control type="email" placeholder="Nazwa użytkownika"/>
                    </Form.Group>

                    <Form.Group controlId="formPassword">
                        <Form.Label>Hasło</Form.Label>
                        <Form.Control type="password" placeholder="Wpisz hasło"/>
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