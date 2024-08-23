const Athlete = require("./models/athlete");
const Account = require("./models/account");
const userArgs = process.argv.slice(2);

const athletes = [];
const accounts = [];

const mongoose = require("mongoose");
mongoose.set("strictQuery", false);

const mongoDB = "mongodb+srv://hofsportsgroupllc:qufy0XXM5n3FMcYw@hofcluster.ejk2lvr.mongodb.net/data?retryWrites=true&w=majority&appName=HOFCluster";

main().catch((err) => console.log(err));

async function athleteCreate(acc, first_name, last_name, phone_number, ig_handle, sport, college, grade,  availability){
    const athletedetail = {
        Account:acc,
        first_name: first_name,
        last_name: last_name,
        phone_number: phone_number,
        ig_handle: ig_handle,
        sport: sport,
        college: college,
        grade: grade,
        availability: availability
    };

    const athlete = new Athlete(athletedetail);

    await athlete.save();
    
    athletes[0] = athlete;

    console.log(`Added athlete: ${first_name} ${last_name}`);
}


async function accountCreate(email,password){

    const accountdetail = {
        email: email,
        password: password
    };

    const account = new Account(accountdetail);
    
    accounts[0] = account;

    accounts[0].save();


    console.log(`Added account with email ${email}`);
}
 

async function main(){
    console.log("About to connect to MongoDB...")

    await mongoose.connect(mongoDB);
    console.log("Should be connected now");

    await accountCreate("bro@gmail.com","lmaowut");
    await athleteCreate(acc = accounts[0],"Asahd", "Hamilton", "123-456-7890", "buglerpack", "Deez", "Denison", "Senior", "None" );
  
}