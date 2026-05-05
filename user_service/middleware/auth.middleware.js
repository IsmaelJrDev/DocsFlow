const jwt = require("jsonwebtoken");

// Middleware para verificar el token JWT
const verifyToken = (req, res, next) => {
  try {
    // Obtener el token del header Authorization
    const token = req.headers.authorization?.split(" ")[1]; // "Bearer <token>"

    if (!token) {
      return res.status(401).json({
        message: "Token no proporcionado",
        error: "Se requiere autenticación"
      });
    }

    // Verificar y decodificar el token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    
    // Guardar el usuario en el request para usarlo después
    req.user = decoded;
    
    next();
  } catch (error) {
    return res.status(403).json({
      message: "Token inválido o expirado",
      error: error.message
    });
  }
};

module.exports = { verifyToken };
