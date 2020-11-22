import React, { Component } from 'react';
import MainPageBanner from "./MainPageBanner";
import MainPageDescription from "./MainPageDescription";

class MainPage extends Component {
    render(){
        return (
            <div>
                <MainPageBanner/>
                <MainPageDescription/>
            </div>
        );
    }
}

export default MainPage;