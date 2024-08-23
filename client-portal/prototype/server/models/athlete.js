const mongoose = require("mongoose")

const Schema = mongoose.Schema;

const athleteSchema = new Schema({
    Account: {type: Schema.Types.ObjectId, ref: "Account", required: false},
    first_name: {type: String, required: true},
    last_name: {type: String, required: true},
    phone_number: {type: String, required: true},
    ig_handle: {type: String, required: true},
    sport: {type: String, required: true},
    college: {type: String, required: true},
    grade: {type: String, required: true},
});


module.exports = mongoose.model("Athlete", athleteSchema);

