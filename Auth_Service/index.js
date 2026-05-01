const dotenv = require("dotenv");
const dotenvExpand = require('dotenv-expand');
const path = require("path");
const express = require("express");
const cors = require("cors");
const mongoose = require("mongoose");
const rutasUsuario = require("./routes/auth.route.js")

const myEnv = dotenv.config({path: path.resolve(__dirname, "../.env")});
dotenvExpand.expand(myEnv);
const app = express();

// Hacemos que el servidor acepte archivos json
app.use(express.json());
app.use(cors());

app.use("/users", rutasUsuario);

// Endpoint donde al ingresar nos mostrara ue funciona correctamente nuestra api
app.get("/", (req, res) => res.json({ message: "Servicio funcional" }));

// Conexión a la base de datos
mongoose.connect(process.env.MONGO_URI)
    .then(() => {
        app.listen(3000, "0.0.0.0", () => console.log("Servidor corriendo"));
    }).catch((err) => {
        console.log("Error al conectar a la base de datos" + err);
    });