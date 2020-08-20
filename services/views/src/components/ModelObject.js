import React from "react";
import {Route, Link} from "react-router-dom";

const axios = require("axios").default;


// WIP => Check if fetch works. Following that, process fetched data and figure out how to
// nicely present results on graph.

class ModelObject extends React.Component {

  constructor(props){
    super(props);
    this.state = {

    }
  }

  fetchModelState = () => {
      axios.get("http://127.0.0.1:5002/model/info/".concat(this.props.model_id.toString()),
                {headers: {"x-access-token": window.localStorage.getItem("x-access-token")}}
      ).then(response => {
          this.setState({
            model_state: response.data.data
          })
      }).catch(error => {
          console.log(error)
          this.setState({
            msg: error.response.data.message
          })
      })
  }

  componentDidMount() {
    this.fetchModelState()
  }

  refresh = () => {
    this.fetchModelState()
  }

  render() {
    const printTestResults = () => {
      if(Boolean(this.state.model_state)){
        return (
          <div id="test">
            <p>Score: {this.state.model_state.test_acc}</p>
            <p>Loss: {this.state.model_state.test_loss}</p>
            <p>Duration: {this.state.model_state.test_duration} seconds</p>
            <p>Time of test: {this.state.model_state.last_test_time}</p>
            <p>Test Device: {this.state.model_state.test_device}</p>
            <p>Status: {this.state.model_state.test_status}</p>
          </div>
        )
      } else {
        return (
          <div id="test">
            <p>Score: N/A</p>
            <p>Loss: N/A</p>
            <p>Duration: N/A</p>
            <p>Time of test: N/A</p>
            <p>Test Device: N/A</p>
            <p>Status: N/A</p>
          </div>
        )
      }
    }
    return (
      <div className="col-md-4">
        <br />
        <div className="card">
          <div className="card-header">
            <span className="float-left">
              <Link to={"/model/".concat(this.props.model_id.toString())}>{this.props.model_title}</Link>
            </span>
            <span className="float-right">
              {this.props.model_framework}
            </span>
          </div>
          <div className="card-body">
            <div>
              <label htmlFor="filename">Deployed Model File:</label>
              <p id="filename">{this.props.name}</p>
            </div>
            <div>
              {printTestResults()}
              <button className="btn btn-default btn-block" onClick={this.refresh}><i className="fa fa-refresh"></i></button>
            </div>
          </div>

        </div>
      </div>
    )
  }
}

export default ModelObject;
