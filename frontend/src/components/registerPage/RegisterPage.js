import React, {Component} from 'react';
import {Form, Button} from "react-bootstrap";

class RegisterPage extends Component {


    render() {
        // TODO na środek to wpierdolić
        return (
            <div className={"align-middle w-responsive"}>
                <Form>
                    <Form.Group controlId="formUsername">
                        <Form.Label>Nazwa użytkownika</Form.Label>
                        <Form.Control type="email" placeholder="Nazwa użytkownika"/>
                    </Form.Group>

                    <Form.Group controlId="formEmail">
                        <Form.Label>Adres e-mail</Form.Label>
                        <Form.Control type="email" placeholder="Wpisz email"/>
                        <Form.Text className="text-muted">
                            Nikomu nie udostępnimy Twojego adresu e-mail.
                        </Form.Text>
                    </Form.Group>

                    <Form.Group controlId="formPassword">
                        <Form.Label>Hasło</Form.Label>
                        <Form.Control type="password" placeholder="Wpisz hasło"/>
                    </Form.Group>

                    <Form.Group controlId="formCheckPassword">
                        <Form.Label>Powtórz hasło</Form.Label>
                        <Form.Control type="password" placeholder="Wpisz jeszcze raz hasło"/>
                    </Form.Group>

                    <Button variant="success" type="submit">
                        Zarejestruj się
                    </Button>
                </Form>
            </div>
        );
    }
}

export default RegisterPage;