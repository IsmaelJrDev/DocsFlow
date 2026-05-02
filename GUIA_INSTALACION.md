# Guía de Instalación y Uso - DocsFlow

## Requisitos Previos

- Docker
- Docker Compose
- Git

## Pasos para Levantar el Proyecto

### 1. Clonar el Repositorio

```bash
git clone https://github.com/IsmaelJrDev/DocsFlow.git
cd DocsFlow
```

### 2. Verificar el Archivo .env

Asegúrate de que el archivo `.env` existe en la raíz del proyecto con estas variables **exactas**:

```
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=password
MONGO_URI=mongodb://admin:password@DocsFlowDatabase1:27017,DocsFlowDatabase2:27017,DocsFlowDatabase3:27017/?replicaSet=rs0&authSource=admin
JWT_SECRET=11jsh701jmDASD93asdasdubgui8798
JWT_EXPIRES_IN=1d
```

### 3. Levantar SOLO los Contenedores de MongoDB (SIN Auth_Service)

Para evitar errores de conexión, levanta solo MongoDB primero:

```bash
docker-compose up -d DocsFlowDatabase1 DocsFlowDatabase2 DocsFlowDatabase3
```

Espera 10 segundos a que MongoDB inicie completamente.

### 4. Inicializar el ReplicaSet de MongoDB

**ESTE PASO ES OBLIGATORIO. Sin él, Auth_Service no podrá conectarse.**

Ejecuta el siguiente comando:

```bash
docker exec DocsFlowDatabase1 mongosh -u root -p 425269qt --eval "rs.initiate({_id: 'rs0', members: [{_id: 0, host: 'DocsFlowDatabase1:27017'}, {_id: 1, host: 'DocsFlowDatabase2:27017'}, {_id: 2, host: 'DocsFlowDatabase3:27017'}]})"
```

**Espera a que termine**. Debería mostrar `{ ok: 1 }`.

### 5. Verificar que el ReplicaSet se Inicializó Correctamente

```bash
docker exec DocsFlowDatabase1 mongosh -u root -p 425269qt --eval "rs.status()"
```

Verifica que aparezca `"state": 1` o `"state": 2` en los miembros. Si ves el error `no replset config has been received`, **vuelve al paso 4**.

### 6. Ahora Sí: Levantar Auth_Service

Una vez confirmado que el ReplicaSet está inicializado, levanta Auth_Service:

```bash
docker-compose up -d Auth_Service
```

### 7. Verificar que Todo Funciona

Revisa los logs del Auth_Service:

```bash
docker logs Auth_Service
```

**Busca este mensaje:**

```
Servidor corriendo
```

Si ves `Error al conectar a la base de datos`, **vuelve al paso 4** para inicializar el ReplicaSet.

---

## Detener el Proyecto

Para detener todos los contenedores:

```bash
docker-compose down
```

Para detener y eliminar también los volúmenes **(borrará la base de datos)**:

```bash
docker-compose down -v
```

---

## Estructura del Proyecto

```
DocsFlow/
├── Auth_Service/          # Microservicio de autenticación (Node.js)
│   ├── index.js
│   ├── package.json
│   ├── models/
│   │   └── User.js
│   └── routes/
│       └── auth.route.js
├── DocsFlowDatabase1/      # Volumen de datos MongoDB 1
├── DocsFlowDatabase2/      # Volumen de datos MongoDB 2
├── DocsFlowDatabase3/      # Volumen de datos MongoDB 3
├── docker-compose.yaml     # Configuración de contenedores
├── mongo-keyfile           # Archivo de clave para seguridad del ReplicaSet
├── .env                    # Variables de entorno
├── README.md               # Documentación general
└── GUIA_INSTALACION.md     # Esta guía
```

---

## Notas Importantes

- El archivo `mongo-keyfile` es necesario para la seguridad del ReplicaSet. Debe tener permisos `400`.
- Los volúmenes de MongoDB persisten los datos entre reinicios de contenedores.
- **La inicialización del ReplicaSet solo necesita hacerse UNA SOLA VEZ** (primera vez).
- Los datos se mantienen en los directorios `DocsFlowDatabase1`, `DocsFlowDatabase2` y `DocsFlowDatabase3`.
- Si borras estos directorios, tendrás que reinicializar el ReplicaSet nuevamente.
