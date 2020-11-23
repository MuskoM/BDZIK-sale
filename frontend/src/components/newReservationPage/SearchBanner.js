import React, {Component} from 'react';
import {Button, Col, Form, Jumbotron} from "react-bootstrap";

class SearchBanner extends Component {
    constructor(props) {
        super(props);
        
    }

    render() {
        return (
            <div>
                <Jumbotron className={"text-center align-middle"}>
                    <h1>Utwórz nową rezerwację</h1>
                    <Form>
                        <Form.Row className={"w-responsive"}>
                            <Col xs={"auto"}>
                                <Form.Control placeholder={"Typ sali"} as={"select"}>
                                    <option>Sala wykładowa</option>
                                    <option>Sala ćwiczeniowa</option>
                                    <option>Pracownia specjalistyczna</option>
                                    <option>Laboratorium</option>
                                </Form.Control>
                            </Col>
                            <Col xs={"auto"}>
                                <Form.Control placeholder={"Od..."}/>
                            </Col>
                            <Col xs={"auto"}>
                                <Form.Control placeholder={"Do..."}/>
                            </Col>
                            <Col xs={"auto"}>
                                <Button type={"submit"}>Szukaj</Button>
                            </Col>
                        </Form.Row>
                        <Form.Row className={"w-responsive"}>
                            <Col>
                                <Form.Text className={"text-right"}>Wyszukiwanie zaawansowane</Form.Text>
                            </Col>
                        </Form.Row>
                        <Form.Row className={"w-responsive"}>
                            <Col>
                                Kurwa test
                            </Col>
                        </Form.Row>
                    </Form>
                </Jumbotron>
            </div>
        );
    }

}

export default SearchBanner;