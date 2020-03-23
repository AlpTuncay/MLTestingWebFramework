import React from "react";
import {Route, Link} from "react-router-dom";

const axios = require("axios").default;


// WIP => Check if fetch works. Following that, process fetched data and figure out how to
// nicely present results on graph.

class ModelObject extends React.Component {

  constructor(props){
    super(props);
    this.state = {
      model_state: []
    }
  }

  fetchModelState = () => {
      axios.get("http://localhost:5002/model/info/".concat(this.props.model_id.toString()),
                {headers: {"x-access-token": window.localStorage.getItem("x-access-token")}}
      ).then(response => {
          this.setState({
            model_state: response.data
          })
          console.log(...this.state.model_state);
      }).catch(error => {
          console.error(error);
      })
  }

  componentDidMount() {
    this.fetchModelState()
  }

  render() {
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
              <label htmlFor="test">Test Results:</label>
              <p id="test">{this.model_state}</p>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default ModelObject;
