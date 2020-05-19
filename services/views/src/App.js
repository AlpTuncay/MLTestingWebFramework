import React from 'react';
import './App.css';
import Register from "./components/Register";
import Login from "./components/Login";
import Home from "./components/Home";
import Main from "./components/Main";
import Logout from "./components/Logout";
import ModelDeployment from "./components/ModelDeployment";
import ModelTest from "./components/ModelTest";

import {Route, Switch, BrowserRouter as Router, Link, Redirect} from "react-router-dom";

const jwt = require("jsonwebtoken");
const axios = require("axios").default;

class App extends React.Component {

    constructor(){
        super();
        this.state = {
            userIsLoggedIn: false
        }
    }

    // This process should be done in the backend.
    validateToken = () => {
        let userToken = "x-access-token" in localStorage ? localStorage.getItem("x-access-token") : "";

        try {
            jwt.verify(userToken, "secret"); //Secret should be changed
            console.log("Valid Token");
            return true;
        } catch (e) {
            console.log("Invalid Token");
            return false;
        }
    };

    componentDidMount() {
        this.setState({
            userIsLoggedIn: this.validateToken()
        });

        if(!this.state.userIsLoggedIn){
            return <Redirect to={"/login"}/>
        }
    }


    render() {
        return (
            <div className="App">
                <div className="container-fluid">
                    <nav className="navbar navbar-expand-lg navbar-light bg-light">
                        <ul className="navbar-nav mr-auto">
                            <li><Link to={'/'} className="nav-link">Home</Link></li>
                            <li>
                                {this.state.userIsLoggedIn ? <Link to={"/model/deploy"} className="nav-link">Deploy Model</Link> : <Link to={'/login'} className="nav-link">Login</Link> }
                            </li>
                            <li>
                                {!this.state.userIsLoggedIn && <Link to={'/register'} className="nav-link">Register</Link>}

                            </li>
                        </ul>
                        <ul className="navbar-nav navbar-right">
                            {this.state.userIsLoggedIn &&
                            <li>
                                <Link to={"/logout"} className="nav-link">Logout</Link>
                            </li>}
                            <li className="nav-link disabled">ML Testing Framework</li>
                        </ul>
                    </nav>
                    <br/>
                    <Switch>
                        <Route exact path='/' component={() => this.state.userIsLoggedIn ? <Main/> : <Home/>}/>
                        {!this.state.userIsLoggedIn ?
                            <Route path='/login' component={() => <Login onSuccess={() => this.setState({userIsLoggedIn: true})}/>}/> : <Route path="/model/deploy" component={() => <ModelDeployment/>}/>}
                        {!this.state.userIsLoggedIn &&
                            <Route path='/register' component={() => <Register/>}/>}
                        {this.state.userIsLoggedIn && <Route path="/logout" component={() => <Logout onLogout={() => this.setState({userIsLoggedIn: false})}/>}/>}
                        <Route path="/model/:id" component={ModelTest}/>
                    </Switch>
                </div>
            </div>
        );
    }
}

export default App;
