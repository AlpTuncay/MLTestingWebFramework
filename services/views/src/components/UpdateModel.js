import React from "react";
import { Redirect } from "react-router-dom";

const axios = require("axios").default;

class UpdateModel extends React.Component {

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
                model_file: event.target.result,
                filename: filename
            })
        }
    };

    getDeployedModelFile = () => {
        axios.get(`http://127.0.0.1:5002/models/${this.props.model_id}`,
            {headers: {"x-access-token": localStorage.getItem("x-access-token")}}
        ).then(response => {
          this.setState({
            current_model_file: response.data.data.filename
          })
        })
    }

    deployBtnOnClick = (event) => {
        event.preventDefault();

        let fileToUpload = this.state.model_file;

        let formData = new FormData();
        formData.append("model_file", fileToUpload);

        console.log(...formData);

        axios.post(`http://127.0.0.1:5002/model/update/${this.props.model_id}`,
            {files: formData.get("model_file"), filename: this.state.filename},
            {headers: {"x-access-token": localStorage.getItem("x-access-token")}}
        ).then(response => {
          this.getDeployedModelFile()
        }).catch(error => {
            console.error(error)
        })
    };

    componentDidMount(){
      this.getDeployedModelFile()
    }

    render() {

        const { redirect, url } = this.state;

        if(redirect){
            return <Redirect to={url}/>
        }

        return (
            <div className="col-md-12">
                <br />
                <div className="card">
                    <div className="card-header">
                      Current deployed model: {this.state.current_model_file}
                    </div>
                    <div className="card-body d-flex justify-content-center">
                        <form className="form-inline" encType="multipart/form-data">
                            <div className="form-group">
                                <input type="file" className="form-control-file" name="model_file" id="model_file" onChange={this.fileUploadHandler}/>
                            </div>
                            <div className="form-group">
                                <button className="btn btn-default btn-success" onClick={this.deployBtnOnClick}>Update Model</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        )
    }
}

export default UpdateModel;
