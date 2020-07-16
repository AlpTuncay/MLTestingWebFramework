import React from "react";
import { Redirect } from "react-router-dom";

const axios = require("axios").default;

class DeviceInfo extends React.Component {

  constructor(props){
    super(props);
    this.state = {
      devices: []
    }
  }

  getInfoOfDevices = () => {
    //axios get request to get devices from ai master service.
    axios.get("http://127.0.0.1:5002/devices",
              {headers: {"x-access-token": window.localStorage.getItem("x-access-token")}}
    ).then(response => {
      console.log(response.data)
      this.setState({
        devices: response.data.queues
      })
    }).catch(error => {
      console.error(error);
    })
  }

  chosenDeviceHandler = (event) => {
    this.props.parentCallback(event.target.value);
  }

  componentDidMount() {
    this.getInfoOfDevices();
  }

  render(){
    return (
      <div className="col-md-12">
          <br />
          <div className="card">
              <div className="card-header d-flex justify-content-center">
                Choose a device
              </div>
              <div className="card-body d-flex justify-content-center form-group">
                <select className="form-control" name="devices" onChange={this.chosenDeviceHandler}>
                  <option value="none" selected disabled hidden>Select an Option</option>
                  {this.state.devices.map((val) => {
                    return <option key={val} value={val}>{val}</option>
                  })}
                </select>
              </div>
          </div>
      </div>
    )
  }

}

export default DeviceInfo;
