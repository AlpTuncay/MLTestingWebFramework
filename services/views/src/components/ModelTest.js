import React from "react";

const axios = require("axios").default;

class ModelTest extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      model_title: "",
      path_to_model: "",
      model_framework: ""

    }
  }

  fetchModelDetails = () => {
    axios.get("http://localhost:5002/models/".concat(this.props.match.params.id.toString()),
              {headers: {"x-access-token": window.localStorage.getItem("x-access-token")}}
    ).then(response => {
      console.log(response.data)
      this.setState({
        model_title: response.data.data.model_title,
        filename: response.data.data.filename,
        model_framework: response.data.data.model_framework
      })
    }).catch(error => {
      console.error(error);
    })
  }

  sendModelTestRequest = () => {
    axios.get(`http://localhost:5002/model/${this.props.match.params.id}/test`,
              {headers: {"x-access-token": window.localStorage.getItem("x-access-token")}}
    ).then(response => {
      console.log(response)
    }).catch(error => {
      console.error(error)
    })
  }

  componentDidMount() {
    this.fetchModelDetails();
  }

  render() {

    return (
        <div className="row d-flex justify-content-center">
          <br />
          <div className="col-md-12">
              <div className="card">
                  <div className="card-body">
                    <h4>Model to be Tested: {this.state.filename}</h4>
                    <button onClick={this.sendModelTestRequest} className="btn btn-default btn-success">Test</button>
                  </div>
              </div>
          </div>
          <div className="col-md-12">
          <br />
            <div className="card">
              <div className="card-body">
                <h3>
                  Get the model specific configuration here. In Keras, if user
                  defined their custom loss function, it should be specified here.
                  Look for these kinds of situations with Tensorflow, PyTorch and Sklearn.
                </h3>
              </div>
            </div>
          </div>
        </div>
    )

  }

}

export default ModelTest;
