import React from "react";


class Model extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="row d-flex justify-content-center">
                <div className="col-md-12">
                    <div className="card">
                        <div className="card-body text-center">
                            <h2>This is the Model page.</h2>
                            <h2>Provides you the possible actions you can take on models such as training and testing.</h2>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

export default Model;