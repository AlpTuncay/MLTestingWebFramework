import React from "react";
import ModelList from "./ModelList"

class User extends React.Component {
    constructor(props) {
        super(props);

    }

    render() {
        return (
            <div className="row d-flex justify-content-center">
                <div className="col-md-12">
                    <div className="card">
                        <div className="card-body">
                            <h3>Welcome {this.props.username}</h3>
                        </div>
                    </div>
                    <ModelList models={this.props.models}/>
                </div>
            </div>
        )
    }
}

export default User;
