import React from "react";
import { Redirect } from "react-router-dom";

const axios = require("axios").default;

class DataUpload extends React.Component {

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
        data_file: event.target.result,
        filename: filename
      })
    }
  };

  uploadBtnOnClick = (event) => {
    //This function sends the request to DataPovider service with the data to upload.
    event.preventDefault();

    let dataFileToUpload = this.state.data_file;

    let formData = new FormData();
    formData.append("data_file", dataFileToUpload);

    axios.post("http://127.0.0.1:5002/data/upload",
                {data: {model_id: this.props.model_id, data_file: formData.get("data_file"), filename: this.state.filename}},
                {headers: {"x-access-token": localStorage.getItem("x-access-token")}}
    ).then(response => {
      this.getAvailableDataForModel()
    }).catch(error => {

    })

  };

  getAvailableDataForModel = () => {

    axios.get(`http://127.0.0.1:5002/model/${this.props.model_id}/data`,
            {headers: {"x-access-token": localStorage.getItem("x-access-token")}}
    ).then(response => {
        this.setState({
          available_data: response.data.data.filename
        });
    }).catch(error => {
      try{
        this.setState({
          msg: error.response.data.message
        });
      } catch {
        this.setState({
          msg: "Error."
        });
      }
    })
  };

  componentDidMount(){
    this.getAvailableDataForModel();
  }

  render(){

    return (
        <div className="col-md-6">
            <br />
            <div className="card">
                <div className="card-header">
                  {Boolean(this.state.available_data) ? `You have uploaded data for this model: ${this.state.available_data}` : `${this.state.msg}.`}
                </div>
                <div className="card-body d-flex justify-content-center">
                    <form className="form-inline" encType="multipart/form-data">
                        <div className="form-group mb-2 mx-sm-3">
                            <input type="file" className="form-control-file" name="data-file" id="data-file" accept=".zip" onChange={this.fileUploadHandler}/>
                        </div>
                        <div className="form-group">
                            <button className="btn btn-default btn-success" onClick={this.uploadBtnOnClick}>Upload Data</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    )
  }

}


export default DataUpload;
