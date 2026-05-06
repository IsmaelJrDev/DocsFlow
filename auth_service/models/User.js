// Definicion de la tabla usuario

const mongoose = require ("mongoose");

const UserSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true
    },
    email: {
        type: String,
        required: true,
        unique: true
    },
    password: {
        type: String,
        required: true
    },
    user_id: {
        type: String,
        unique: true
    },
    role: {
        type: String,
        enum: ["secretariat", "admin"],
        default: "secretariat"
    }
})


module.exports = mongoose.model("User", UserSchema);