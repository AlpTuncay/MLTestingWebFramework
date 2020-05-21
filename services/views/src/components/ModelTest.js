import React from "react";
import { Redirect } from "react-router-dom";
import DataUpload from "./DataUpload";
import TestConfigUpload from "./TestConfigUpload";
import TestGraph from "./TestGraph";
import UpdateModel from "./UpdateModel";

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
    axios.get("http://127.0.0.1:5002/models/".concat(this.props.match.params.id.toString()),
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
    axios.get(`http://127.0.0.1:5002/model/${this.props.match.params.id}/test`,
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
        <div className="row">
          <TestGraph model_id={this.props.match.params.id}/>
        </div>
        <div className="row">
          <UpdateModel model_id={this.props.match.params.id}/>
        </div>
        <div className="row">
          <TestConfigUpload model_id={this.props.match.params.id}/>
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
