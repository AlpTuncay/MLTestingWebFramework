import React from "react";
import { Redirect } from "react-router-dom";

const axios = require("axios").default;

class UpdateCustomObjects extends React.Component {

    constructor(props) {
        super(props);
        this.state = { }
    }

    formInputChangeHandler = (event) => {
        this.setState({
            [event.target.name]: event.target.value
        })
    };

    fileUploadHandler = (event) => {
        let fileReader = new FileReader();
        fileReader.readAsDataURL(event.target.files[0]);
        let filename = event.target.files[0].name;
        fileReader.onload = (event) => {
            this.setState({
                custom_objects: event.target.result,
                filename: filename
            })
        }
    };

    getDeployedCustomObjectsFile = () => {
        axios.get(`http://127.0.0.1:5002/models/${this.props.model_id}`,
            {headers: {"x-access-token": localStorage.getItem("x-access-token")}}
        ).then(response => {
          this.setState({
            current_objects_file: response.data.data.custom_objects_filename
          })
        })
    }

    deployBtnOnClick = (event) => {
        event.preventDefault();

        let fileToUpload = this.state.custom_objects;

        let formData = new FormData();
        formData.append("custom_objects", fileToUpload);

        console.log(...formData);

        axios.post(`http://127.0.0.1:5002/model/update/custom_objects/${this.props.model_id}`,
            {files: formData.get("custom_objects"), custom_objects_filename: this.state.filename},
            {headers: {"x-access-token": localStorage.getItem("x-access-token")}}
        ).then(response => {
          this.getDeployedCustomObjectsFile()
        }).catch(error => {
            console.error(error)
        })
    };

    componentDidMount(){
      this.getDeployedCustomObjectsFile()
    }

    render() {

        const { redirect, url } = this.state;

        if(redirect){
            return <Redirect to={url}/>
        }

        var message = "No deployed file";
        if(Boolean(this.state.current_objects_file)){
          message = this.state.current_objects_file
        }

        return (
            <div className="col-md-6">
                <br />
                <div className="card">
                    <div className="card-header">
                      Current deployed custom objects file: {message}
                    </div>
                    <div className="card-body d-flex justify-content-center">
                        <form className="form-inline" encType="multipart/form-data">
                            <div className="form-group">
                                <input type="file" className="form-control-file" name="custom_objects" id="custom_objects" accept=".py" onChange={this.fileUploadHandler}/>
                            </div>
                            <div className="form-group">
                                <button className="btn btn-default btn-success" onClick={this.deployBtnOnClick}>Update Custom Objects</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
          )
    }
}

export default UpdateCustomObjects;
