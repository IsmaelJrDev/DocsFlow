// Archivo de rutas para app
const router = require("express").Router();
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const User = require("../models/User.js");
const { response } = require("express");

// Endpoint para registrar usuario con metodo post
router.post("/register", async(req, res)=>{
    try{
        const {name, email, password, role} = req.body;
        const passhash = await bcrypt.hash(password, 10);

        // Validar que el role sea válido
        const validRoles = ["secretariat", "admin"];
        const userRole = validRoles.includes(role) ? role : "secretariat";

        // Creación de un usuario
        const mongoose = require("mongoose");
        const _id = new mongoose.Types.ObjectId();
        const user = await User.create({
            _id,
            user_id: _id.toString(),
            name,
            email, 
            password: passhash,
            role: userRole
        })

        res.status(201).json({message: "Usuario creado", user: {
            _id: user._id,
            name: user.name,
            email: user.email,
            role: user.role
        }})

    }catch (error){
        // Si existe algun usuario con el mismo correo
        if (error.code === 11000) {
        return res.status(400).json({
            error: "El correo ya tiene una cuenta registrada",
        });
        }

        res.status(400).json({
            message: "Error al registrar usuario" + error.message || " "
        });
    }
})

router.post("/login", async(req, res)=>{
    try{
        const {email, password} = req.body;

        const user = await User.findOne({email});

        // Si no se encuentra el usuario
        if (!user) return res.status(404).json({
            message: "Usuario no encontrado"
        });

        // Verificamos que el usuario tenga contraseña (por si se corrompió)
        if (!user.password) {
            return res.status(401).json({
                message: "La cuenta no tiene contraseña válida, contacta al administrador."
            });
        }

        // Comparar contraseña hash y no hash
        const valid = await bcrypt.compare(password, user.password);

        // Si la contraseña no es valida
        if (!valid) return res.status(401).json({
            message: "Usuario o contraseña incorrectos"
        })

        // Generamos el token
        const token = jwt.sign(
            {id:user._id, email:user.email},
            process.env.JWT_SECRET,
            {expiresIn: process.env.JWT_EXPIRES_IN}
        )

        // Si todo esta correcto
        res.status(200).json({
            token,
            user: {
                _id: user._id,
                name: user.name,
                email: user.email,
                role: user.role
            }
        })
    }catch(error){
        // Si existe algun otro error interno
        res.status(500).json({
            message: error.message || "No pudo procesarse la solicitud"
        })
    }
});

module.exports = router;