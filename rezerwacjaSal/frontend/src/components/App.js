import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import Topbar from "./Topbar";

class App extends Component{
    render() {
        return (
                    <div className={"w-responsive mx-auto p-3 mt-2"}>
              <Topbar />
          </div>
        );
    }
}

ReactDOM.render(<App/>,document.getElementById('app'))