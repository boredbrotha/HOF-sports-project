import React, {useState} from "react";
import axios from 'axios';
import {Link} from 'react-router-dom';
import hoflogo from '../images/hoflogo.png'
axios.defaults.withCredentials = true;


function Forgot(){

    /* 
    Forgot Page
    -----------

    Function: This page is the forgot password page for the HOF Sports client portal.
              It emails the user their password if their credentials exist in the system.
    */


    const [sentVerification, setSentVerification] = useState(false);
    const [email, setEmail] = useState("");

    const [message, setMessage] = useState("");

    const handleEmailChange = (event) => {

        const value = event.target.value;
        setEmail(value);

    }

    async function submit(e){
        e.preventDefault();

        const credentials = {"Email":email, "sentVerification": sentVerification};

        try{
            await axios.post("http://localhost:8000/forgot", credentials)
            .then(res => {

                if (res.data === "badEmail"){
                    setMessage("This Email doesn't exist in our system. Please try again.")
                }
                else if((res.data === "emailSent") && (sentVerification === false)){
                    setMessage("We just sent an an email to your inbox containing your password. If you didn't get it, please refresh and try again.")
                    

                    setSentVerification(true);

                }
                else{
                    setMessage("Your account is verified already. Go and log in!")
                }
            }).catch ( e => {
                alert("wrong details");
                console.log(e);
            });
        }catch{
            console.log(e);
        }
    }

    return (
        <div className="main">

            <div className="hofImage">

                <img src={hoflogo} alt="HOF Sports Logo"/>
            </div>

            <form className="forgot-form" action = "POST" onSubmit={submit}>

                <div className="forgot-field">

                    <input type="email" value = {email} onChange={handleEmailChange} placeholder="Input Email Here..." />   
                </div>  

                <div className="submit-field">

                    <input type="submit" value="Submit" />
                </div>
                
                <p>{message}</p>
            </form>

            <div className="forgot-bottom-section">

                <Link to={"/login"}>
                    <input className="back-to-login" type="button" value="Back to Login"/>
                </Link>
            </div>
        </div>
    )
}

export default Forgot;