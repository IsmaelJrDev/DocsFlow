const express = require('express');
const router = express.Router();
const bcrypt = require('bcrypt'); // Asegúrate de tener instalado npm install bcrypt
const User = require('../models/User'); 

// 1. Endpoint para MOSTRAR la información (Para la Pantalla 1)
router.get('/:id', async (req, res) => {
  try {
    const userId = req.params.id;
    
    // Buscamos al usuario en la base de datos
    const user = await User.findByPk(userId); // Si usas Sequelize (PostgreSQL)
    // const user = await User.findById(userId); // Usa esto si es Mongoose (MongoDB)

    if (!user) {
      return res.status(404).json({ message: 'Usuario no encontrado' });
    }

    // Retornamos los datos SIN la contraseña por seguridad
    res.json({
      id: user.id,
      name: user.name,
      email: user.email,
      role: user.role
    });

  } catch (error) {
    res.status(500).json({ message: 'Error al obtener el perfil', error: error.message });
  }
});

// 2. Endpoint para GUARDAR la edición (Para la Pantalla 2)
router.put('/:id', async (req, res) => {
  try {
    const userId = req.params.id;
    
    // Extraemos SOLO lo que permitimos editar del body (ignoramos el rol si lo envían)
    const { name, email, password } = req.body;

    // Buscamos el usuario
    let user = await User.findByPk(userId); // Cambia a findById si es Mongo
    if (!user) {
      return res.status(404).json({ message: 'Usuario no encontrado' });
    }

    // Actualizamos nombre y correo si vienen en la petición
    if (name) user.name = name;
    if (email) user.email = email;

    // Lógica para el candado: Solo encriptar y guardar si el usuario escribió una nueva
    if (password && password.trim() !== "") {
      const salt = await bcrypt.genSalt(10);
      user.password = await bcrypt.hash(password, salt);
    }

    // Guardamos en la base de datos
    await user.save();

    res.json({ message: 'Perfil actualizado correctamente' });

  } catch (error) {
    res.status(500).json({ message: 'Error al actualizar el perfil', error: error.message });
  }
});

module.exports = router;