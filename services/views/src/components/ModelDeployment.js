import React from "react";

const axios = require("axios").default;

class ModelDeployment extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            model_title: "",
            model_framework: "",
            model_file: ""
        }
    }

    formInputChangeHandler = (event) => {
        this.setState({
            [event.target.name]: event.target.value
        })
    };

    render() {
        return (
            <div className="row d-flex justify-content-center">
                <div className="col-md-12">
                    <div className="card">
                        <div className="card-body d-flex justify-content-center">
                            <div className="form-horizontal">
                                <div className="form-group">
                                    <label htmlFor="model_title" className="control-label">Model Title</label>
                                    <input id="model_title" className="form-control" name="model_title" type="text" onChange={this.formInputChangeHandler} required/>
                                </div>
                                <div className="form-group">
                                    <label htmlFor="model_framework" className="control-label">Model Framework</label>
                                    <select className="form-control" name="model_framework" onChange={this.formInputChangeHandler}>
                                        <option value="Keras">Keras</option>
                                        <option value="Sklearn">Sklearn</option>
                                        <option value="PyTorch">PyTorch</option>
                                    </select>
                                </div>
                                <div className="form-group">
                                    <label htmlFor="model_file" className="control-label">Model Definition File</label>
                                    <input type="file" className="form-control-file" name="model_file" id="model_file" onChange={this.formInputChangeHandler}/>
                                </div>
                                <div className="form-group">
                                    <button type="file" className="btn btn-default btn-success">Deploy</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

export default ModelDeployment;