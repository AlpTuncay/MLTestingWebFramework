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
        path_to_model: response.data.data.path,
        model_framework: response.data.data.model_framework
      })
    }).catch(error => {
      console.error(error);
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
                    <h4>Title: {this.state.model_title}</h4>
                    <h4>Path: {this.state.path_to_model}</h4>
                    <h4>Framework: {this.state.model_framework}</h4>
                  </div>
              </div>
          </div>
          <br />
          <div className="col-md-12">
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
