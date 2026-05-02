const express = require("express");
const router = express.Router();
const User = require("../models/User.js");

// GET: Obtener todos los perfiles de usuario
router.get("/", async (req, res) => {
    try {
        const usuarios = await User.find();
        res.json(usuarios);
    } catch (error) {
        res.status(500).json({ message: "Error al obtener usuarios", error: error.message });
    }
});

// GET: Obtener perfil por user_id (Importante para la trazabilidad del sistema)
router.get("/:user_id", async (req, res) => {
    try {
        // Buscamos por el campo personalizado user_id definido en el modelo
        const usuario = await User.findOne({ user_id: req.params.user_id });
        if (!usuario) {
            return res.status(404).json({ message: "Usuario no encontrado" });
        }
        res.json(usuario);
    } catch (error) {
        res.status(500).json({ message: "Error al obtener el usuario", error: error.message });
    }
});

// POST: Crear un nuevo perfil
router.post("/", async (req, res) => {
    try {
        const nuevoUsuario = new User(req.body);
        const usuarioGuardado = await nuevoUsuario.save();
        res.status(201).json(usuarioGuardado);
    } catch (error) {
        res.status(400).json({ message: "Error al crear el perfil", error: error.message });
    }
});

// PUT: Actualizar un perfil por su ID de MongoDB
router.put("/:id", async (req, res) => {
    try {
        const usuarioActualizado = await User.findByIdAndUpdate(
            req.params.id, 
            req.body, 
            { new: true } // Esto devuelve el documento ya actualizado
        );
        if (!usuarioActualizado) {
            return res.status(404).json({ message: "Usuario no encontrado" });
        }
        res.json(usuarioActualizado);
    } catch (error) {
        res.status(400).json({ message: "Error al actualizar el usuario", error: error.message });
    }
});

// DELETE: Eliminar un perfil (Dar de baja)
router.delete("/:id", async (req, res) => {
    try {
        const usuarioEliminado = await User.findByIdAndDelete(req.params.id);
        if (!usuarioEliminado) {
            return res.status(404).json({ message: "Usuario no encontrado" });
        }
        res.json({ message: "Usuario eliminado correctamente" });
    } catch (error) {
        res.status(500).json({ message: "Error al eliminar el usuario", error: error.message });
    }
});

module.exports = router;