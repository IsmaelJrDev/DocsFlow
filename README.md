# 📌 DocFlow

Sistema distribuido de automatización, análisis y gestión de flujo documental.

## 📖 Descripción

**DocFlow** es una plataforma diseñada para resolver la problemática de gestión documental en oficinas, automatizando la lectura, clasificación y priorización de documentos mediante inteligencia artificial. El sistema garantiza eficiencia y organización, reduciendo el tiempo operativo y los errores humanos.

La arquitectura se fundamenta en microservicios contenedorizados y un pipeline de IA local, cumpliendo estrictamente con el requisito de ejecución **100% offline** (sin conexión a internet).

## 🏗️ Arquitectura del Sistema

El sistema está diseñado bajo un modelo distribuido para asegurar la alta disponibilidad y el procesamiento concurrente:

* **API Gateway (Nginx):** Punto de entrada único, enrutamiento y balanceo de carga.
* **Microservicios (Node.js):**
    * **Auth Service:** Gestión de roles (Escritura/Lectura) y sesiones JWT.
    * **User Service:** Administración de perfiles.
    * **Document Service:** Orquestador principal que gestiona la carga de archivos y la comunicación con el pipeline de IA.
* **Pipeline de IA (Ollama):** Ejecución local de modelos para:
    * Análisis de contenido.
    * Generación de resúmenes automáticos.
    * Clasificación de prioridad (Rojo, Ámbar, Verde).
* **Persistencia (MongoDB):** Almacenamiento NoSQL para documentos, metadatos y etiquetas de prioridad.

## 🛠️ Tecnologías Utilizadas

| Categoría | Tecnología | Uso en el proyecto |
| :--- | :--- | :--- |
| **Backend** | Node.js (NestJS) | Microservicios transaccionales. |
| **IA Local** | Ollama | Pipeline de inferencia (Offline). |
| **Base de Datos** | MongoDB | Persistencia orientada a documentos. |
| **Gateway** | Nginx | API Gateway / Reverse Proxy. |
| **Infraestructura** | Docker & Compose | Orquestación de clúster de 3 máquinas. |

## 📂 Estructura del Proyecto

```text
DocFlow/
├── auth_service/          # Microservicio de Autenticación
├── user_service/          # Gestión de usuarios y permisos
├── doc_service/           # Orquestador de IA y archivos
├── nginx/                 # Configuración de Nginx
├── docker-compose.yml     # Orquestación del sistema distribuido
└── README.md              # Documentación técnica

```

## 🚀 Instalación y Despliegue Local
Clonar el repositorio:

```Bash
git clone <url-del-repositorio>
cd DocFlow
``
Despliegue del Clúster:
```Bash
docker-compose up --build -d
```
Nota: El sistema está configurado para operar totalmente offline. Asegúrate de tener los pesos del modelo de IA cargados en el volumen de persistencia.

## 📝 Especificaciones de Evaluación (FO-ACA-13-4)
Ejecución Offline: Todo el pipeline, incluyendo Ollama, corre dentro de la red local definida en Docker.

Sistema de Prioridad:

🔴 Rojo: Alta prioridad (Requiere acción inmediata).

🟡 Ámbar: Prioridad media.

🟢 Verde: Baja prioridad (Informativo).

Auditoría: Cada documento registrado incluye timestamp y user_id para trazabilidad completa.

## 🤝 Contribución
Sigue el flujo de trabajo definido en CONTRIBUTING.md. Todo PR debe incluir tests unitarios que validen el procesamiento de la IA local.
