const mongoose = require("mongoose")

const Schema = mongoose.Schema;

const accountSchema = new Schema({
    email: {type:String, required:true, maxLength:100},
    password: {type:String, required:true, maxLength: 100},
    verified: {type:Boolean, required:true}
});


module.exports = mongoose.model("Account", accountSchema);