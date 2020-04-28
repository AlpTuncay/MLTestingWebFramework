import React from "react";
import { Redirect } from "react-router-dom";

const axios = require("axios").default;


class CreateModelTestConfig extends React.Component {

  constructor(props){
    super(props);
    this.state = {}
  }

  fileUploadHandler = (event) => {
    //This is the function to read zip files for uploading.
    let fileReader = new FileReader();
    fileReader.readAsDataURL(event.target.files[0]);

    let filename = event.target.files[0].name

    fileReader.onload = (event) => {
      this.setState({
        config_file: event.target.result,
        filename: filename
      })
    }
  };

  getAvailableConfig = () => {

    axios.get(`http://localhost:5002/test/config/${this.props.model_id}`,
            {headers: {"x-access-token": localStorage.getItem("x-access-token")}}
    ).then(response => {
        this.setState({
          available_config: response.data.available_config
        });
    }).catch(error => {
      console.log(error)
      this.setState({
        msg: error.response.data.message
      });
    })
  };

  uploadConfigOnClick = (event) => {
      event.preventDefault();

      let fileToUpload = this.state.config_file;

      let formData = new FormData();
      formData.append("config_file", fileToUpload);

      console.log(...formData);

      axios.post("http://localhost:5002/test/config",
          {data: {model_id: this.props.model_id, config_file: formData.get("config_file"), filename:this.state.filename}},
          {headers: {"x-access-token": localStorage.getItem("x-access-token")}}
      ).then(response => {
        this.setState({
          available_config: response.data.data.filename
        })
      }).catch(error => {

      })
  };

  componentDidMount(){
    this.getAvailableConfig();
  }

  render(){

    return (

      <div className="col-md-6">
          <br />
          <div className="card">
              <div className="card-header">
                {Boolean(this.state.available_config) ? `You have already provided config: ${this.state.available_config}` : `${this.state.msg} Please provide a JSON config file.`}
              </div>
              <div className="card-body d-flex justify-content-center">
                  <form className="form-inline" encType="multipart/form-data">
                      <div className="form-group mb-2 mx-sm-3">
                          <input type="file" className="form-control-file" name="data-file" id="data-file" onChange={this.fileUploadHandler}/>
                      </div>
                      <div className="form-group">
                          <button className="btn btn-default btn-success" onClick={this.uploadConfigOnClick}>Upload Config</button>
                      </div>
                  </form>
              </div>
          </div>
      </div>

    )

  }

}

export default CreateModelTestConfig;
