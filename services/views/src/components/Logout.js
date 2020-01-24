import {Redirect} from "react-router-dom";
import React from "react";

function Logout(props) {
    console.log(localStorage.getItem("x-access-token"));
    window.localStorage.removeItem("x-access-token");
    console.log("Removed token");
    props.onLogout();

    return <Redirect to="/"/>
}

export default Logout;