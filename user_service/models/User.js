const mongoose = require("mongoose");

const userSchema = new mongoose.Schema({
    name: { 
        type: String 
    },
    email: { 
        type: String, 
        required: true, 
        unique: true 
    },
    password: {
        type: String
    },
    role: { 
        type: String, 
        enum: ["secretariat", "admin", "secretaria"], 
        default: "secretariat" 
    },
    user_id: { 
        type: String 
    }
}, {
    // Esto garantiza la trazabilidad/auditoría con timestamp (creación y edición)
    timestamps: true 
});

module.exports = mongoose.model("User", userSchema);