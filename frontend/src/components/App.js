import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import Topbar from "./Topbar";
import {HashRouter as Router, Route, Switch, Redirect} from 'react-router-dom'
import MainBanner from "../components/mainPage/MainPageBanner"
import Description from "../components/mainPage/MainPageDescription";

class App extends Component{
    render() {
        return (
             <div className={"w-responsive mx-auto p-3 mt-2"}>
              <Topbar />
              <Router>
                  <div className="cointainer">
                      <Switch>
                          <Route path='/new' component={Description}/>
                      </Switch>
                  </div>
                  <MainBanner />
              </Router>
          </div>
        );
    }
}

ReactDOM.render(<App/>,document.getElementById('app'))