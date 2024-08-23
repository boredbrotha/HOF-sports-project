

// Set up mongoose
const mongoose = require("mongoose");
mongoose.set("strictQuery", false);
const mongoDB = "mongodb+srv://hofsportsgroupllc:qufy0XXM5n3FMcYw@hofcluster.ejk2lvr.mongodb.net/data?retryWrites=true&w=majority&appName=HOFCluster";

//Set up express and its middleware
const express = require("express")
const cors = require("cors");
const session = require("express-session");

//Set up the mongoose models we'll be using
const account = require("./models/account");
const athlete = require("./models/athlete");

//Set up utility functions
const sendVerificationEmail = require("./util/verification-email");
const sendForgotEmail = require("./util/forgot-email");




//Initialize the express app
const app = express();
app.use(express.json());
app.use(express.urlencoded({extended: true}));

//Initialize CORS
app.use(
  cors({
    origin: "http://localhost:3000",
    methods: ["GET", "POST"],
    credentials: true,
  })
);


//Initialize express-session
app.use(
  session({
    key: "userId",
    secret: "subscribe",
    resave: false,
    saveUninitialized: false,
    cookie: {
      expires: 60 * 60 * 24,
    },
  })
);




app.get("/",cors(), (req,res) =>{
  res.json("hello");
})



app.get("/loggedin", async(req,res) => {
  //This handles requests pertaining to whether a user's session is still up.


  console.log("DEBUG: Just got a GET request for '/loggedin'.")

  if (req.session.user){ //If a session exists
    
    let userEmail = req.session.user;

    //We access the mongoDB model with the user's email, then we access the athlete model attached to it.
    const emailObject =  await account.findOne({email:userEmail});
    const athleteObject = await athlete.findOne({Account:emailObject._id});

    res.send({loggedIn:true,name:athleteObject.first_name});
  }
  else{
    res.send({loggedIn: false});
  }
})


app.get("/logout", async(req, res) => {
  //This handles log-out requests.

  console.log("DEBUG: Just got a GET request for '/logout' ")
  
  req.session.destroy((err) => {
    if (err) {
      console.log("Error destroying session: ", err);
      res.json("unsuccessful")
    }
    else{
      res.clearCookie('userId');
      res.json("successful");
    }
  })
})



app.post("/login",async(req,res) => {
  //This handles log-in requests.


  console.log("DEBUG: Just got a POST request for '/login' ")
  const{email, password} = req.body;

  try {
    
    const emailCheck = await account.findOne({email:email, password: password});



    
    if(emailCheck){
      if(emailCheck.verified === false){
        console.log("DEBUG: --POST /login-- This email isn't verified.")
        res.json("notverified");
      }
      else{
        console.log("DEBUG: --POST /login-- This email is verified. Creating a session, then redirecting the user to the dashboard.");

        req.session.user = emailCheck.email;
        console.log(req.session.user);
        res.json("exist");
      }

    } 
    else{
      console.log("DEBUG: --POST /login-- The account associated with the email doesn't exist.")
      res.json("notexist");
    }


  } catch (e) {
    res.json("fail");
  }
});


app.post("/signup", async(req,res) => {
  //This handles sign-up requests

  console.log("DEBUG: --POST /signup-- Just got a POST request for /signup");

  //Receive and store the credentials received from the front-end
  const signupCredentials = req.body;


  const emailCheck = await account.findOne({email:signupCredentials["Email"]})
  try{
    if(emailCheck){
      console.log("DEBUG: --POST /signup-- Account already exists");
      res.json("exist");
    }

    else if( (signupCredentials['Email'].indexOf('@') === -1) ||
             (signupCredentials['Email'].indexOf('.') === -1) )
             {
                console.log("DEBUG: --POST /signup-- User inputted their email incorrectly");
                res.json("badEmail")
             }
    else{
      console.log("DEBUG: --POST /signup-- Account doesn't exist yet. Creating new account");

      //We begin the process of creating a new entry in the mongoDB database.

      var newAccount = new account({email: signupCredentials["Email"], password: signupCredentials["Password"], verified: false});
      var newAthlete = new athlete({
        Account: newAccount, //It's very important that we link the new account to the new athlete.
        first_name : signupCredentials["First Name"],
        last_name : signupCredentials["Last Name"],
        phone_number : signupCredentials["Phone Number"],
        ig_handle : signupCredentials["Handle"],
        sport : signupCredentials["Sport"],
        college: signupCredentials["College"],
        grade: signupCredentials["Class"],
      })

      console.log("DEBUG: --POST /signup-- Awaiting a save...");

      await newAthlete.save();
      console.log("DEBUG: --POST /signup-- Saved the athlete");
      await newAccount.save();
      console.log("DEBUG: --POST /signup-- Saved the account");

      //After everything is successfully executed, we send a verification email to the user. 
      await sendVerificationEmail(newAccount.email, newAccount._id);

      res.json("notExist");

  }
  }catch(e){
    res.json("fail");
  }
});

app.post("/forgot", async(req,res) =>{
  console.log("Just got a forgot password POST from the client");
  const reqEmail = req.body

  console.log(reqEmail);
  const emailCheck = await account.findOne({email:reqEmail["Email"]});

  try{
    if((emailCheck) && (reqEmail["sentVerification"] === false)){

      await sendForgotEmail(reqEmail["Email"],emailCheck.password);

      console.log("Just sent that email");

      res.json("emailSent");
    }
    else{
      res.json("badEmail")
    }
  }catch(e){
    res.json("fail");
  }


});


app.get('/verify/:userID', async (req, res) => {
  //This GET request handles verifying an account

  const {userID} = req.params;

  try{
    //We attempt to find the account given the userID we pulled from the request's parameters.
    let userAccount = await account.findById(userID);

    if (!userAccount){
      res.json("invalidlink");
    }

    else{
      userAccount.verified = true;
      await userAccount.save();

      res.redirect('http://localhost:3000/login')
    }

  }catch(e){
    res.json("serverfail")
  }
});


app.listen(8000, () => {
  console.log("Application is listening on port 8000...");
  mongoose.connect(mongoDB);
})



