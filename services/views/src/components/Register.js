import React from "react";
import {Redirect} from "react-router-dom";

const axios = require("axios").default;

class Register extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: "",
            email: "",
            name: "",
            surname: "",
            password: ""
        }
    }

    formInputChangeHandler = (event) => {
        this.setState({
            [event.target.name]: event.target.value
        })
    };


    /***
     * This is where the POST request to the http://register:5000/register sent
     */
    registerBtnOnClick = (event) => {
        event.preventDefault();
        axios.post(
            'http://localhost:5002/register',
            {data: this.state}
        ).then(response => {
            this.setState({
                redirect: true,
                message: response.data["message"]
            })

        }).catch(error => {
            console.log(error.response["message"])
        });
    };

    render() {
        const {redirect} = this.state;

        if(redirect){
            return <Redirect to="/login"/>
        }
        return (
            <div className="row d-flex justify-content-center">
                <div className="col-md-5">
                    <div className="card">
                        <div className="card-body">
                            <form className="form-horizontal" content="application/json">
                                <div className="form-group">
                                    <label htmlFor="username" className="control-label">Username:</label>
                                    <div className="col-md-12">
                                        <input id="username" className="form-control" name="username" type="text" placeholder="Username" onChange={this.formInputChangeHandler} required />
                                    </div>
                                </div>
                                <div className="form-group">
                                    <label htmlFor="email" className="control-label">Email:</label>
                                    <div className="col-md-12">
                                        <input id="email" className="form-control" name="email" type="email" placeholder="xxx@xxx.com" onChange={this.formInputChangeHandler} required/>
                                    </div>
                                </div>
                                <div className="form-group">
                                    <label htmlFor="name" className="control-label">Name:</label>
                                    <div className="col-md-12">
                                        <input id="name" className="form-control" name="name" type="text" placeholder="Name" onChange={this.formInputChangeHandler} required/>
                                    </div>
                                </div>
                                <div className="form-group">
                                    <label htmlFor="surname" className="control-label">Surname:</label>
                                    <div className="col-md-12">
                                        <input id="surname" className="form-control" name="surname" type="text" placeholder="Surname" onChange={this.formInputChangeHandler} required/>
                                    </div>
                                </div>
                                <div className="form-group">
                                    <label htmlFor="password" className="control-label">Password:</label>
                                    <div className="col-md-12">
                                        <input id="password" className="form-control" name="password" type="password" placeholder="Password" onChange={this.formInputChangeHandler} required/>
                                    </div>
                                </div>
                                <div className="form-group">
                                    <button onClick={this.registerBtnOnClick} className="btn btn-default btn-success">Register</button>
                                </div>
                            </form>
                        </div>
                    </div>
                    <div className="row d-flex justify-content-center">
                        {this.state.message}
                    </div>
                </div>
            </div>
        );
    }
}

export default Register
