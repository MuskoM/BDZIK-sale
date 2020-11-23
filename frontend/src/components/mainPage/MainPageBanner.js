import React, {Component} from "react";
import {Jumbotron, Form, Col, Button} from "react-bootstrap";
import "../../css/index.css"

class MainPageBanner extends Component {
    render() {
        const background = 'https://d-pt.ppstatic.pl/k/r/1/3b/d4/5fae540cce000_p.jpg';
        const jumbotronStyle = {
            color: "white",
            background: "url(" + background + ") center center",
            backgroundSize: "cover",
        };

        return(
            <Jumbotron className={"text-center"} style={jumbotronStyle}>
                <h1><b>Zarezerwuj salę na Politechnice Białostockiej</b></h1>
                <p>Wypróbuj nowy system rezerwacji pomieszczeń na największej uczelni technicznej we wschodniej Polsce!</p>
            </Jumbotron>
        )
        // TODO wyśrodkowanie formularza wyszukiwania na głównej stronie
    }
}

export default MainPageBanner;