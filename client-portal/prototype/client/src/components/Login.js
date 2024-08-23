import React, {useState} from "react";
import axios from 'axios';
import {useNavigate, Link} from 'react-router-dom';
import hoflogo from '../images/hoflogo.png'


axios.defaults.withCredentials = true;



function Login() {
    /* 
    Login Page:
    -----------

    Function: This component represents the login page for the HOF Sports client portal.
              Users will input their account credentials here. If they're in our database,
              we will begin a session for them to be able to access and traverse the HOF dashboard.
    */



    const history = useNavigate();


    //useStates for form credentials
    const [email, setEmail] = useState('');
    const[showPassword,setShowPassword] = useState(false);
    const [password, setPassword] = useState('');
    



    const handleEmailChange = (event) => {
        
        const value = event.target.value;
        setEmail(value);
    }

    const handlePasswordChange = (event) => {
        
        const value = event.target.value;
        setPassword(value);

    }

    async function submit(e){
        e.preventDefault();

        try{
            //We attempt a POST to see if the inputted credentials are in HOF's MongoDB Database
            await axios.post("http://localhost:8000/login",{email,password})
            .then(res => {
                if(res.data === "exist"){
                    history("/",{state:{id:email}});
                }
                else if(res.data === "notexist"){
                    alert("User hasn't signed up..");
                }
            })
            .catch( e => {
                alert("wrong details");
                console.log("Error: " + e);
            })
        }
        catch(e){
            console.log(e);
        }
    }


    return(
        <div className ="main">

            <div className="hofImage">

                <img src={hoflogo} alt="HOF Sports Logo"/>
            </div>
            <div className="login-box">

                <form className="login-form" action="POST" onSubmit={submit}> 

                    <div className="input-field">

                        <label>Email</label>
                        <input type="email" onChange={handleEmailChange} />
                    </div>

                    <div className="input-field">

                        <label>Password</label>
                        <input  type={showPassword ? "text" : "password"} value = {password}   onChange = {handlePasswordChange} />
                        <input className = "show-password" type="button" value = "Show" onClick={() => setShowPassword((prev) => !prev)} maxLength={100} />
                    </div>
                    <div className="submit-field">

                        < input type= "submit" value = "Login"/>
                    </div>
                </form>

                <div className="bottom-section">

                    <Link to={"/forgot"}>
                        <input className="forgot-redirect" type="button" value="Forgot Password?"/>
                    </Link>

                    <Link to={"/signup"}>
                        <input className="signup-redirect" type = "button" value="No account? Sign-up here." />
                    </Link>
                </div>
            </div>
        </div>
    )
}


export default Login;