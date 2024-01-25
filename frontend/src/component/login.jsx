import React from "react";
import "../assets/css/login.css"
import "../assets/css/App.css"
import { Link } from "react-router-dom";
import loginimg from "../assets/img/login.png"

const href="https://gymkhana.iitb.ac.in/profiles/oauth/authorize/?client_id=GrPHTL6apOjMxGVxK8JINy755G7LbZBKsEGS0ho4&response_type=code&scope=profile picture ldap program&redirect_uri=https://itc.gymkhana.iitb.ac.in/certificates/0"

export default function  Login(){
    return(
        <div className="login">
            <header> ITC Certificate Portal 23-24</header>
            <div className='box-wrapper login-wrapper'>
                <Link to={href} className='boxes'><div className='box'>SSO LOGIN</div></Link>
            </div>
            <img src={loginimg} className="loginimg"alt="" srcSet="" />
            
            <div className='login-footer footer container'>
            Developed by the Web Team with &#128155; | Institute Technical Council 2023
            </div>
        </div>
    )
}
