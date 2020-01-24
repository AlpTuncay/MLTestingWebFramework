import React from 'react';
import './App.css';
import Register from "./components/Register";
import Login from "./components/Login";
import Home from "./components/Home";
import Main from "./components/Main";
import {Route, Switch, BrowserRouter as Router, Link} from "react-router-dom";

const jwt = require("jsonwebtoken");

class App extends React.Component {

    constructor(){
        super();
        this.state = {
            userIsLoggedIn: false
        }
    }

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
        })
    }

    render() {
        return (
            //If there is a valid token in the localStorage, based on that render a different navbar.
            <div className="App">
                <Router>
                    <div>
                        <nav className="navbar navbar-expand-lg navbar-light bg-light">
                            <ul className="navbar-nav mr-auto">
                                <li><Link to={'/'} className="nav-link">Home</Link></li>
                                <li>
                                    {this.state.userIsLoggedIn ? <Link to={"/model/deploy"} className="nav-link">Deploy Model</Link> : <Link to={'/login'} className="nav-link">Login</Link> }
                                </li>
                                <li>
                                    {this.state.userIsLoggedIn ? <Link to={"/model/test"} className="nav-link">Test Model</Link> : <Link to={'/register'} className="nav-link">Register</Link>}

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
                            <Route path='/login' component={() => <Login/>}/>
                            <Route path='/register' component={() => <Register/>}/>
                            {this.state.userIsLoggedIn && <Route path='/profile' component={() => <Main />}/>}
                        </Switch>
                    </div>
                </Router>
            </div>
        );
    }
}

export default App;
