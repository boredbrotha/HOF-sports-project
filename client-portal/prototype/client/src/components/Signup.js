import React, { useState} from "react";
import axios from 'axios';
import {useNavigate, Link} from 'react-router-dom';
import hoflogo from '../images/hoflogo.png'


axios.defaults.withCredentials = true;



function Signup() {

    /* 
    Signup Page:
    ------------

    Function: This component represents the signup page for the HOF Sports client portal.
              Users will be able to input their credentials here, and upon a successful
              sign-up, the user's information will be stored in HOF's MongoDB Database.
    */
    const history = useNavigate();
    const [showPassword, setShowPassword] = useState(false);



    //These are useState hooks for the information typed into the form fields.
    const [emailField, setEmailField] = useState("");
    const [passwordField, setPasswordField] = useState("");
    const [fNameField, setFNameField] = useState("");
    const [lNameField, setLNameField] = useState("");
    const [numberField, setNumberField] = useState("");
    const [handleField, setHandleField] = useState("");
    const [sportField, setSportField] = useState("");
    const [collegeField, setCollegeField] = useState("");
    const [classField, setClassField] = useState("");


    //These red text useState hooks are for the various errors that might appear while a user inputs their information.
    const [redText0, setRedText0] = useState("");
    const [redText1, setRedText1] = useState("");
    const [redText2, setRedText2] = useState("");

    const handleEmailChange = (event) => {
        
        const value = event.target.value;
        setEmailField(value);
    }

    const handlePasswordChange = (event) => {
        
        const value = event.target.value;
        setPasswordField(value);

    }

    const handleFNameChange = (event) => {
        
        const value = event.target.value;
        setFNameField(value);
    }

    const handleLNameChange = (event) => {
        
        const value = event.target.value;
        setLNameField(value);
    }


    function formatNumber(value){
        // If there's no value, we return that empty value.
        if (!value) return value;

        //Clean input for non-zero values
        const phoneNumber = value.replace(/[^\d]/g, '');


        const phoneNumberLength = phoneNumber.length;

        //If the value inputted is less than 4 in length, no formatting is needed
        if (phoneNumberLength < 4) return phoneNumber;


        //If the inputted value is between 4 and 7, we begin to format it.
        if (phoneNumberLength < 7) {
            return `(${phoneNumber.slice(0, 3)}) ${phoneNumber.slice(3)}`;
        }

        
        //We do the full formatting if the length is longer than 7.
        return `(${phoneNumber.slice(0, 3)}) ${phoneNumber.slice(3,6)}-${phoneNumber.slice(6, 10)}`;
    }

    const handleNumberChange = (event) => {


        const formattedNumber = formatNumber(event.target.value)
        setNumberField(formattedNumber);

    }

    const handleHandleChange = (event) => {
        
        const value = event.target.value;
        setHandleField(value);
    }

    const handleSportChange = (event) => {
        
        const value = event.target.value;
        setSportField(value);
    }

    const handleCollegeChange = (event) => {
        
        const value = event.target.value;
        setCollegeField(value);
    }

    const handleClassChange = (event) => {

        const value = event.target.value;

        const formattedValue = value.replace(/[^\d]/g, '');


        setClassField(formattedValue);
    }

    async function submit(e){


        e.preventDefault(); //Quick Prevent Default
        

        //This boolean goes to true if anything problematic happens within the following if-statements.
        let potentialIssue = false;  

        if (handleMissingFields().length !== 0){
            
            var missingFields = handleMissingFields();
            var cuteString = "";
            console.log(missingFields.length);

            for(let i = 0; i<missingFields.length; i++){
                cuteString += missingFields[i]
                if (i!==missingFields.length-1){
                    cuteString += ", "
                }

                
            }

            setRedText0("You haven't filled out all the fields. The fields you left blank are:" + cuteString); //Fix this \n issue at some point
            potentialIssue = true;
        }

        var credentials = {
            "Email" :  emailField,
            "Password" : passwordField,
            "First Name" : fNameField,
            "Last Name" : lNameField,
            "Phone Number" : numberField,
            "Handle" :  handleField,
            "Sport" : sportField,
            "College" : collegeField,
            "Class" : classField
        }

        if ((credentials["Password"].length < 8)){
            setRedText2("Your password must be between 8 and 100 characters long.")
            potentialIssue = true
        }

        if (potentialIssue){
            return 0;
        }

        //We try to POST the credentials to the server
        try{ 
            await axios.post("http://localhost:8000/signup", credentials) 
            .then(res => {

                //In the case that an error is thrown, I clear these fields so there won't be extra red text on the screen if a prior submit failed.
                setRedText0('');
                setRedText1('');


                if(res.data === "badEmail"){

                    setRedText1("You inputted your email incorrectly. Please try again.")

                }

                if(res.data === "exist"){ 

                    setRedText1("This email already exists in the database. Please try again.");

                }
                else if(res.data === "notExist"){
                    
                    history("/verify",{state:{id:emailField}}); //Redirect to the verification page.

                    
                }

                //After we're done, we clear the form.
                setEmailField('');
                setPasswordField('');
                setFNameField('');
                setLNameField('');
                setNumberField('');
                setHandleField('');
                setSportField('');
                setCollegeField('');
                setClassField('');

                return 0;
            })
            .catch(e => {
                alert("wrong details")
                console.log(e);
            })
        }
        catch(e){
            console.log(e);
        }

        //After everything is done, we clear the fields in the form.
        setEmailField('');
        setPasswordField('');
        setFNameField('');
        setLNameField('');
        setNumberField('');
        setHandleField('');
        setSportField('');
        setCollegeField('');
        setClassField('');

        

    }

    function handleMissingFields(){
        /* So, this function returns the fields that are missing in the form, then returns an array of strings containing which ones. */

        var missingFields = []

        if ( emailField === ""){
            missingFields.push("Email") 
        }
        if ( passwordField === ""){
            missingFields.push("Password")
        }
        if ( fNameField === ""){
            missingFields.push("First Name")
        }
        if ( lNameField === ""){
            missingFields.push("Last Name")
        }
        if ( numberField === ""){
            missingFields.push("Phone Number")
        }
        if ( handleField === ""){
            missingFields.push("IG Handle")
        }
        if ( sportField === ""){
            missingFields.push("Sport")
        }
        if ( collegeField === ""){
            missingFields.push("College")
        }
        if ( classField === ""){
            missingFields.push("Class")
        }

        return missingFields

    }

    return(
        <div className="main">

            <div className="hofImage">
                <img src={hoflogo} alt="HOF Sports Logo"/>
                
            </div>

            <div className="signup-box">
                <form className = "signup-form" action = "POST" onSubmit={submit}>

                    <div className="input-field">
                        <label>Email</label>
                        <input type="email" value={emailField}   onChange = {handleEmailChange} required maxLength={100} />
                    </div>

                    <div className="input-field">
                        <label>Password</label>
                        <input  type={showPassword ? "text" : "password"} value = {passwordField}   onChange = {handlePasswordChange} />
                        <input className = "show-password" type="button" value = "Show" onClick={() => setShowPassword((prev) => !prev)} maxLength={100} />
                    </div>

                    <div className="input-field">
                        <label>First Name</label>
                        <input type="text" value={fNameField} onChange={handleFNameChange} maxLength={30}  />
                    </div>
                

                    <div className="input-field">
                        <label>Last Name</label>
                        <input  type="text" value={lNameField} onChange={handleLNameChange} maxLength={20}   />
                    </div>


                    <div className="input-field">
                        <label>Phone Number</label>
                        <input type = "tel" value={numberField} onChange={handleNumberChange} />
                    </div>

                    <div className="input-field">
                        <label>Instagram</label>
                        <input  type="text" value={handleField} onChange={handleHandleChange} maxLength={30} />
                    </div>
            
                    <div className="input-field">
                        <label>Sport</label>
                        <input  type="text" value={sportField} onChange={handleSportChange} maxLength={30}  />
                    </div>

                    <div className="input-field">
                        <label>College</label>
                        <input type="text" value={collegeField} onChange={handleCollegeChange}  />
                    </div>

                    <div className="input-field">
                        <label>Class Year</label>
                        <input type="text" value={classField} onChange={handleClassChange} maxLength={4}   />
                    </div>


                    <div className="submit-field">
                        <input type="submit" value="Create Account" />
                    </div>



                </form>
                <p className="redText">{redText0}</p>
                <p className="redText">{redText1}</p>
                <p className="redText">{redText2}</p>

                <div className="login-section">

                <Link to = "/login">
                    <input className="login-redirect" type="button" value="Already have an account?" />
                </Link>


                </div>

            </div> 



        </div>




    )
}

export default Signup;