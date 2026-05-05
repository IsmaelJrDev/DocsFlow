const mongoose = require("mongoose");

const userSchema = new mongoose.Schema({
    name: { 
        type: String, 
        required: true 
    },
    email: { 
        type: String, 
        required: true, 
        unique: true 
    },
    role: {
        type: String,
        enum: ["secretariat", "admin"],
        default: "secretariat"
    },
    user_id: { 
        type: String, 
        required: true,
        unique: true
    },
    password: {
        type: String,
        required: true
    
    },
}, {
    // Esto garantiza la trazabilidad/auditoría con timestamp (creación y edición)
    timestamps: true 
});

module.exports = mongoose.model("User", userSchema);