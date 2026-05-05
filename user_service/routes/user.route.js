const express = require('express');
const router = express.Router();
const bcrypt = require('bcrypt');
const User = require('../models/User');
const { verifyToken } = require('../middleware/auth.middleware');

// 1. Endpoint para MOSTRAR la información (Para la Pantalla 1)
// Requiere autenticación con JWT
router.get('/:id', verifyToken, async (req, res) => {
  try {
    const userId = req.params.id;
    
    // Buscamos al usuario en la base de datos
    const user = await User.findById(userId);

    if (!user) {
      return res.status(404).json({ message: 'Usuario no encontrado' });
    }

    // Retornamos los datos SIN la contraseña por seguridad
    res.json({
      _id: user._id,
      name: user.name,
      email: user.email,
      role: user.role,
      user_id: user.user_id
    });

  } catch (error) {
    res.status(500).json({ message: 'Error al obtener el perfil', error: error.message });
  }
});

// 2. Endpoint para GUARDAR la edición (Para la Pantalla 2)
// Requiere autenticación con JWT
router.put('/:id', verifyToken, async (req, res) => {
  try {
    const userId = req.params.id;
    
    // Extraemos SOLO lo que permitimos editar del body
    const { name, email, password } = req.body;

    // Buscamos el usuario
    let user = await User.findById(userId);
    if (!user) {
      return res.status(404).json({ message: 'Usuario no encontrado' });
    }

    // Actualizamos nombre y correo si vienen en la petición
    if (name) user.name = name;
    if (email) user.email = email;

    // Si el usuario no tiene user_id (documento antiguo), asignamos el _id
    if (!user.user_id) {
      user.user_id = user._id.toString();
    }

    // Lógica para el candado: Solo encriptar y guardar si el usuario escribió una nueva
    if (password && password.trim() !== "") {
      const salt = await bcrypt.genSalt(10);
      user.password = await bcrypt.hash(password, salt);
    }

    // Guardamos en la base de datos
    await user.save();

    res.json({ message: 'Perfil actualizado correctamente', user: {
      _id: user._id,
      name: user.name,
      email: user.email,
      role: user.role
    }});

  } catch (error) {
    res.status(500).json({ message: 'Error al actualizar el perfil', error: error.message });
  }
});

module.exports = router;