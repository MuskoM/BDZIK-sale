import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import Topbar from "./Topbar";
import MainBanner from "./MainBanner";
import Description from "./Description";

class App extends Component{
    render() {
        return (
                    <div className={"w-responsive mx-auto p-3 mt-2"}>
              <Topbar />
              <MainBanner />
              <Description/>
          </div>
        );
    }
}

ReactDOM.render(<App/>,document.getElementById('app'))