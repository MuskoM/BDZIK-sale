import React, { Component } from 'react';
import {Table} from "react-bootstrap"

class SearchTable extends Component {
    constructor(props) {
        super(props);
        this.state = {
            foundRoomsList: [
                
            ]
        }
    }


    render(){
        return (
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>Sala</th>
                        <th>Budynek</th>
                        <th>Typ sali</th>
                        <th>Liczba miejsc</th>
                        <th>Atrybuty</th>
                    </tr>
                </thead>
            </Table>
        );}
}