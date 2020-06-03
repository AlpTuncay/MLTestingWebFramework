import React from "react";


class Home extends React.Component {

    render() {
        return (
            <div className="row d-flex justify-content-center">
                <div className="col-md-8">
                    <div className="panel panel-default">
                        <div className="panel-heading">
                            <h4>This framework can be used for testing the AI models developed locally.</h4>
                        </div>
                        <div className="panel-body">
                            <ol>
                                <li>Deploy your model, right now supports Keras and Sklearn.</li>
                                <li>Choose which hardware you wish to test your model.</li>
                                <li>Run your tests.</li>
                            </ol>
                        </div>
                    </div>
                </div>
            </div>
        )
    }

}

export default Home;
