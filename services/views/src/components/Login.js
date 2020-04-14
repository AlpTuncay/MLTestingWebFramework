import React from "react";
import {Redirect} from "react-router-dom";

const axios = require("axios").default;

class Login extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            email: "",
            password: "",
            redirect: false,
            url: "",
            message: ""

        }
    }

    formInputChangeHandler = (event) => {
        this.setState({
            [event.target.name]: event.target.value
        })
    };

    loginBtnOnClick = (event) => {
        //Send request to API /login endpoint
        //Get the response back and save the JWT to localStorage
        event.preventDefault();
        axios.post("http://localhost:5002/login",
            {data: this.state}
        ).then(response => {
            this.setState({
                redirect: true,
                url: "/"
            });
            localStorage.setItem("x-access-token", response.data.token);
            this.props.onSuccess();
            console.log(response.data.token)
        }).catch(error => {
            console.log(error);
            this.setState({
                message: error.response.data["message"]
            })
        });
    };

    render() {
        const { redirect } = this.state;

        if(redirect){
            return <Redirect to={this.state.url} />
        }
        return (
            <div className="row d-flex justify-content-center">
                <div className="col-md-5">
                    <div className="card">
                        <div className="card-body text-center">
                            <div className="form-horizontal" id="login-form">
                                <div className="form-group">
                                    <label htmlFor="user_email" className="control-label">Email:</label>
                                    <div className="col-md-12">
                                        <input id="user_email" className="form-control" name="email" type="email" placeholder="xxx@xxx.com" onChange={this.formInputChangeHandler} required />
                                    </div>
                                </div>
                                <div className="form-group">
                                    <label htmlFor="user_passwd" className="control-label">Password:</label>
                                    <div className="col-md-12">
                                        <input id="user_passwd" className="form-control" name="password" type="password" placeholder="Password" onChange={this.formInputChangeHandler} required />
                                    </div>
                                </div>
                                <div className="form-group">
                                    <button className="btn btn-default btn-success" onClick={this.loginBtnOnClick}>Login</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="row d-flex justify-content-center">
                        {this.state.message}
                    </div>
                </div>
            </div>
        )
    }
}

export default Login;
