import React from "react";
import User from "./User";

const axios = require("axios").default;

class Main extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            username: "",
            name: "",
            surname: "",
            models: []
        }
    }

    fetchUser = () => {
        console.log("Requesting with " + window.localStorage.getItem("x-access-token"));
        axios.get(
            "http://127.0.0.1:5002/user/profile",
            {headers: {"x-access-token": window.localStorage.getItem("x-access-token")}}
        ).then(response => {
            console.log(response.data);
            this.setState({
                username: response.data.user.username,
                name: response.data.user.name,
                surname: response.data.user.surname,
                models: response.data.models
            });
            console.log(...this.state.models)
        }).catch(error => {
            console.log(error);
        })
    };

    componentDidMount() {
        this.fetchUser();
    }

    render() {
        return (
            <User name={this.state.name}
                  surname={this.state.surname}
                  username={this.state.username}
                  models={this.state.models}
            />
        )
    }
}

export default Main;
