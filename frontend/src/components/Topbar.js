import React, {Component} from "react";
import {Button, Container, Nav, Navbar} from "react-bootstrap";

class Topbar extends Component {
    render() {
        return(
            <Container fluid className={"TopBar"}>
                <div className={"TopNavBar"}>
                    <Navbar bg="light" expand="lg">
                        <Navbar.Brand><img src={"https://navoica.pl/static/images/org/Politechnika%20Bia%C5%82ostocka.png"} style={{width: "30%", height: "30%"}}/></Navbar.Brand>
                        <Nav className={"ml-auto"}>
                            <Button variant={"link"} style={{float: "right"}}>Zarejestruj się</Button>
                            <Button variant={"primary"} style={{float: "right"}}>Zaloguj się</Button>
                        </Nav>
                    </Navbar>
                </div>
                <div className={"BottomNavBar"}>
                    <Navbar bg="light" expand="lg">

                        <Navbar.Toggle aria-controls={"basic-navbar-nav"}/>
                        <Navbar.Collapse id={"basic-navbar-nav"}>
                            <Nav className={"mr-auto"}>
                                <Nav.Link href={"#home"}>Strona główna</Nav.Link>
                                <Nav.Link href={"#home"}>Nowa rezerwacja</Nav.Link>
                                <Nav.Link href={"#home"}>Twoje rezerwacje</Nav.Link>
                            </Nav>
                            <Nav className={"ml-auto"}>
                                <Nav.Link href={"{% link %}"}>Ustawienia konta</Nav.Link>
                            </Nav>
                        </Navbar.Collapse>
                    </Navbar>
                </div>
            </Container>
        )
    }
}

export default Topbar;