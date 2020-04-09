import React from "react";
import { Redirect } from "react-router-dom";
import DataUpload from "./DataUpload";

const axios = require("axios").default;

class ModelTest extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      model_title: "",
      path_to_model: "",
      model_framework: "",
      redirect: false,
      url: "/"
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
      this.setState({
        redirect: true
      })
    }).catch(error => {
      console.error(error)
    })
  }

  componentDidMount() {
    this.fetchModelDetails();
  }

  render() {
    const { redirect, url } = this.state;

    if(redirect){
        return <Redirect to={url}/>
    }
    return (
      <div>
        <div className="row d-flex justify-content-center">
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

        <div className="row">
          <DataUpload model_id={this.props.match.params.id}/>
          <br />
        </div>
        <div className="row">
          <div className="col-md-12">
            <br />
            <button onClick={this.sendModelTestRequest} className="btn btn-default btn-success btn-block">Test</button>
          </div>
        </div>
      </div>
    )

  }

}

export default ModelTest;