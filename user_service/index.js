const dotenv = require("dotenv");
const dotenvExpand = require('dotenv-expand');
const path = require("path");
const express = require("express");
const mongoose = require("mongoose");

// Importamos tus rutas de usuario/perfil
const rutasPerfil = require("./routes/user.route.js");

// Configuración de variables de entorno apuntando a la raíz del proyecto (igual que Auth_Service)
const myEnv = dotenv.config({path: path.resolve(__dirname, "../.env")});
dotenvExpand.expand(myEnv);

const app = express();

// Middlewares: Hacemos que el servidor acepte JSON y habilitamos CORS
app.use(express.json());

// Definimos la ruta base para este microservicio. 
// Nota: Le puse "/perfiles" para diferenciarlo del "/users" de tu compañero, 
// pero pueden ajustarlo según lo que defina su API Gateway (Nginx).
app.use("/perfiles", rutasPerfil);

// Endpoint de prueba para verificar que el contenedor levantó bien
app.get("/", (req, res) => res.json({ message: "User Service funcional" }));

// Conexión a la base de datos y arranque del servidor
mongoose.connect(process.env.MONGO_URI)
    .then(() => {
        // Usamos un puerto distinto al 3000 para evitar conflictos locales
        const PORT = process.env.USER_PORT || 3000; 
        app.listen(PORT, "0.0.0.0", () => console.log(`Servidor User Service corriendo en puerto ${PORT}`));
    }).catch((err) => {
        console.log("Error al conectar a la base de datos: " + err);
    });