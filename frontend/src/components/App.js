import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import Topbar from "./Topbar";
import {HashRouter as Router, Route, Switch, Redirect} from 'react-router-dom'
import MainPage from "./mainPage/MainPage";
import NewReservationPage from './newReservationPage/NewReservationPage'

class App extends Component {
    render() {
        return (
            <div className={"w-responsive mx-auto p-3 mt-2 container"}>
                <Topbar/>
                <Router>
                    <div>
                        <Switch>
                            <Route exact path='/' component={MainPage}/>
                            <Route exact path='/new' component={NewReservationPage}/>
                            <Route exact path='/cokolwiek'><p>Cokolwiek</p></Route>
                        </Switch>
                    </div>
                </Router>
            </div>
        );
    }
}

ReactDOM.render(<App/>, document.getElementById('app'))