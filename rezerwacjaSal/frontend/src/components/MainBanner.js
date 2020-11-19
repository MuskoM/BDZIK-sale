import React, {Component} from "react";
import {Jumbotron, Form, Col, Button} from "react-bootstrap";

class MainBanner extends Component {
    render() {
        return(
            <Jumbotron className={"text-center"} >
                <h1><b>Zarezerwuj salę na Politechnice Białostockiej</b></h1>
                <p>Wypróbuj nowy system rezerwacji pomieszczeń na największej uczelni technicznej we wschodniej Polsce!</p>
                <Form>
                    <Form.Row className={"align-center w-responsive"}>
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
                </Form>
            </Jumbotron>
        )
        // TODO wyśrodkowanie formularza wyszukiwania na głównej stronie
    }
}

export default MainBanner;