import React, {Component} from "react";
import {Media} from "react-bootstrap"

class MainPageDescription extends Component {
    render() {
        return (
            <div className={"w-75 mx-auto"}>
                <Media>
                    <Media.Body>
                        <h1>System rezerwacji PB</h1>
                        <p>
                            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse vitae fringilla massa, eget dignissim nisi. Nullam ornare risus et ipsum laoreet interdum. Phasellus eget laoreet felis, tincidunt tempor nisi. Duis eget condimentum est, ac pretium orci. Suspendisse finibus at nisi sit amet tincidunt. Nullam laoreet rutrum tellus. Duis quis malesuada quam. Mauris ac sapien eu urna porta convallis vitae finibus lorem. Sed malesuada condimentum sapien at dignissim. Nunc vulputate sagittis urna, vel pretium urna vulputate non.
                        </p>
                        <p>
                            Suspendisse potenti. Mauris viverra urna et nisl mollis laoreet. Nam non tellus sed nibh hendrerit sodales sed mollis orci. Suspendisse a interdum ipsum, et commodo ligula. Sed a fringilla risus, et posuere sem. In hac habitasse platea dictumst. Morbi elementum velit est. Fusce quis dapibus orci. Integer neque sapien, posuere vel quam eget, lobortis suscipit mi. Interdum et malesuada fames ac ante ipsum primis in faucibus.
                        </p>
                    </Media.Body>
                    <img width={360} height={300} className={"w-responsive mr-3"} src={"https://iph.bialystok.pl/wp-content/uploads/2019/11/logo-PB.png"}/>
                </Media>
            </div>
        )
    }

}

export default MainPageDescription;