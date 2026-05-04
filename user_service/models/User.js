const mongoose = require("mongoose");

const userSchema = new mongoose.Schema({
    nombre: { 
        type: String, 
        required: true 
    },
    email: { 
        type: String, 
        required: true, 
        unique: true 
    },
    rol: { 
        type: String, 
        enum: ["Lectura", "Escritura", "Admin"], 
        default: "Lectura" 
    },
    user_id: { 
        type: String, 
        required: true,
        unique: true
    }
}, {
    // Esto garantiza la trazabilidad/auditoría con timestamp (creación y edición)
    timestamps: true 
});

module.exports = mongoose.model("User", userSchema);