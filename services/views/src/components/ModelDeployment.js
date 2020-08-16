import React from "react";
import { Redirect } from "react-router-dom";

const axios = require("axios").default;

class ModelDeployment extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            model_title: "",
            model_framework: "",
            model_file: null,
            custom_objects_file: null,
            redirect: false,
            url: "/"
        }
    }

    formInputChangeHandler = (event) => {
        this.setState({
            [event.target.name]: event.target.value
        })
    };

    modelFileUploadHandler = (event) => {
        let fileReader = new FileReader();
        fileReader.readAsDataURL(event.target.files[0]);
        let filename = event.target.files[0].name;
        fileReader.onload = (event) => {
            this.setState({
                model_file: event.target.result,
                filename: filename
            })
        }
    };

    customObjectsFileUploadHandler = (event) => {
        let fileReader = new FileReader();
        fileReader.readAsDataURL(event.target.files[0]);
        let filename = event.target.files[0].name;
        fileReader.onload = (event) => {
            this.setState({
                custom_objects_file: event.target.result,
                custom_objects_filename: filename
            })
        }
    };

    deployBtnOnClick = (event) => {
        event.preventDefault();

        let configFileToUpload = this.state.model_file;
        let customObjectsFileToUpload = this.state.custom_objects_file;

        let formData = new FormData();
        formData.append("model_file", configFileToUpload);
        formData.append("custom_objects_file", customObjectsFileToUpload);
        formData.append("model_title", this.state.model_title);
        formData.append("model_framework", this.state.model_framework);

        console.log(...formData);

        if (this.state.custom_objects_file === null) {
          var postData = {data: {"model_title": formData.get("model_title"),
                            "model_framework": formData.get("model_framework")},
                            "files": {"model_file": formData.get("model_file")},
                            "filename": this.state.filename}
        } else {
          var postData = {data: {"model_title": formData.get("model_title"),
                            "model_framework": formData.get("model_framework")},
                            "files": {"model_file": formData.get("model_file"), "custom_objects_file": formData.get("custom_objects_file")},
                            "filename": this.state.filename, "custom_objects_filename": this.state.custom_objects_filename}
        }


        axios.post("http://127.0.0.1:5002/model/deploy",
            postData,
            {headers: {"x-access-token": localStorage.getItem("x-access-token")}}
        ).then(response => {
            this.setState({
                redirect: true
            })
        }).catch(error => {
            console.error(error)
        })
    };

    render() {

        const { redirect, url } = this.state;

        if(redirect){
            return <Redirect to={url}/>
        }

        return (
            <div className="row">
                <div className="col-md-12">
                    <div className="card">
                        <div className="card-body d-flex justify-content-center">
                            <form className="form-horizontal" encType="multipart/form-data">
                                <div className="form-group">
                                    <label htmlFor="model_title" className="control-label">Model Title</label>
                                    <input id="model_title" className="form-control" name="model_title" type="text" onChange={this.formInputChangeHandler} required/>
                                </div>
                                <div className="form-group">
                                    <label htmlFor="model_framework" className="control-label">Model Framework</label>
                                    <select className="form-control" name="model_framework" onChange={this.formInputChangeHandler}>
                                        <option value="none" selected disabled hidden>Select an Option</option>
                                        <option value="Keras">Keras</option>
                                        <option value="Sklearn">Sklearn</option>
                                    </select>
                                </div>
                                <div className="form-group">
                                    <label htmlFor="model_file" className="control-label">Model Definition File</label>
                                    <input type="file" className="form-control-file" name="model_file" id="model_file" onChange={this.modelFileUploadHandler}/>
                                </div>
                                <div className="form-group">
                                    <label htmlFor="custom_objects_file" className="control-label">If you have custom objects in your model, please provide .py file with implementations</label>
                                    <input type="file" className="form-control-file" name="custom_objects_file" id="custom_objects_file" onChange={this.customObjectsFileUploadHandler}/>
                                </div>
                                <div className="form-group">
                                    <button className="btn btn-default btn-success" onClick={this.deployBtnOnClick}>Deploy</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

export default ModelDeployment;
