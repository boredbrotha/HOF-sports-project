import React, {useEffect, useState} from "react";
import axios from 'axios';
import {useNavigate} from 'react-router-dom';
axios.defaults.withCredentials = true;



function Home() {

    /*
    
    Home Page
    ---------

    Function: This is the defacto dashboard page for the HOF Sports client portal.
              It currently prints the logged-in user's first name, and has log-out
              functionality.
    */
    const [name, setName] = useState("");
    const navigate = useNavigate();

    async function handleLogout(){
        try{
            await axios.get("http://localhost:8000/logout")
            .then(res => {
                if (res.data === "successful"){
                    window.location.reload();
                }
                else{
                    alert("something went wrong. please refresh and try again.")
                }
            }).catch(e => {
                alert("server error");
                console.log(e)
            })
                
            
        }catch(e){
            console.log(e)
        }
    }

    //This useEffect() checks to see whether the session associated with the logged in user is up.
    useEffect(() => {
        axios.get("http://localhost:8000/loggedin").then((res) => {
            if (res.data.loggedIn === true) {
                setName("Hello, " + res.data.name);

            }
            else{
                setName("No account detected. Redirecting to login..")
                navigate("/login");
            }
        });
    });

    return(
        <div className="home">

            <p>{name}</p>

            <input className="logout-button" type="button" value={"Log out"} onClick={handleLogout} />
        </div>
    )
}



export default Home;