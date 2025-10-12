# API de Alquiler de Vehículos

Sistema de gestión para alquiler de autos, motos y bicicletas con autenticación JWT y campos de auditoría.

## Nuevas Características

### 🔐 Autenticación JWT
- Sistema completo de login/register
- Tokens JWT para autorización
- Middleware de autenticación en endpoints protegidos

### 🗃️ Base de Datos Normalizada
- **Estados de alquiler**: Tabla normalizada (`estado_alquiler`) con estados: activo, completado, cancelado
- **Roles de usuario**: Tabla `roles` con administrador, empleado, usuario
- **Campos de auditoría**: Todas las tablas principales incluyen `creado_por`, `actualizado_por`, `fecha_creacion`, `fecha_actualizacion`

### 👥 Gestión de Usuarios
- Tabla `auth_usuarios` para autenticación
- Tabla `usuario` para información de perfil
- Sistema de roles y permisos

## 🚀 Instalación y Configuración

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Inicializar Base de Datos
```bash
python init_data.py
```

Este script creará:
- Todas las tablas necesarias
- Estados de alquiler por defecto
- Roles por defecto  
- Usuario administrador inicial

### 3. Credenciales Iniciales
**Usuario Administrador:**
- Username: `admin`
- Password: `admin123`
- Email: `admin@sistema.com`

⚠️ **IMPORTANTE**: Cambia la contraseña después del primer login.

### 4. Ejecutar la API
```bash
python main.py
```

La API estará disponible en: `http://localhost:8000`
Documentación Swagger: `http://localhost:8000/docs`

## 📋 Endpoints de Autenticación

### POST /auth/register
Registra un nuevo usuario
```json
{
  "username": "nuevo_usuario",
  "email": "user@email.com", 
  "password": "password123",
  "nombre_completo": "Nombre Completo",
  "rol_id": 2
}
```

### POST /auth/login
Autentica un usuario
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Respuesta:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1Q...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": "uuid",
    "username": "admin",
    "email": "admin@sistema.com",
    "nombre_completo": "Administrador",
    "activo": true,
    "rol_id": 1
  }
}
```

### GET /auth/me
Obtiene información del usuario actual (requiere autenticación)

### GET /auth/verify  
Verifica si el token es válido (requiere autenticación)

## 🔒 Autenticación en Endpoints

Para usar endpoints protegidos, incluye el token en el header:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

## 📊 Cambios en la Base de Datos

### Nuevas Tablas
- `estado_alquiler` - Estados normalizados
- `roles` - Roles de usuario  
- `auth_usuarios` - Usuarios para autenticación

### Campos Añadidos
Todas las tablas principales ahora incluyen:
- `creado_por` - ID del usuario que creó el registro
- `actualizado_por` - ID del usuario que actualizó el registro  
- `fecha_creacion` - Timestamp de creación
- `fecha_actualizacion` - Timestamp de última actualización

### Cambios en Relaciones
- `alquileres.estado` → `alquileres.estado_id` (FK a `estado_alquiler`)
- `usuario.rol` → `usuario.rol_id` (FK a `roles`)
- Todos los IDs ahora son UUID (String de 36 caracteres)

## 🛠️ Configuración de Seguridad

### Cambiar Clave Secreta
En `utils/auth_utils.py`, actualiza:
```python
SECRET_KEY = "tu_clave_secreta_muy_segura_aqui"
```

### Configurar Tiempo de Expiración
```python  
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutos
```

## 📝 Ejemplos de Uso

### 1. Registrar Usuario
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "empleado1",
    "email": "empleado@empresa.com",
    "password": "password123",
    "nombre_completo": "Juan Pérez",
    "rol_id": 2
  }'
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

### 3. Crear Alquiler (con autenticación)
```bash
curl -X POST "http://localhost:8000/alquileres/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": "cliente_uuid",
    "vehiculo_id": "vehiculo_uuid", 
    "fecha_inicio": "2024-01-15",
    "fecha_fin": "2024-01-20",
    "observaciones": "Alquiler de fin de semana"
  }'
```

## 🔧 Estados y Roles

### Estados de Alquiler
1. **Activo** - Alquiler en curso
2. **Completado** - Alquiler finalizado 
3. **Cancelado** - Alquiler cancelado

### Roles de Usuario
1. **Administrador** - Acceso total al sistema
2. **Empleado** - Acceso a operaciones
3. **Usuario** - Acceso básico

## ⚡ Próximas Mejoras

- [ ] Middleware de permisos por rol
- [ ] Logs de auditoría detallados
- [ ] Recuperación de contraseña
- [ ] Refresh tokens
- [ ] Rate limiting
- [ ] Validación avanzada de permisos por endpoint

## 🐛 Solución de Problemas

### Error: "Token inválido"
- Verifica que el token esté en el header `Authorization: Bearer TOKEN`
- Confirma que el token no haya expirado

### Error: "Usuario no encontrado"  
- Ejecuta `python init_data.py` para crear el usuario admin
- Verifica las credenciales de login

### Error de Base de Datos
- Elimina `database.db` y ejecuta `python init_data.py` nuevamente
- Verifica que todas las dependencias estén instaladas

## 📞 Soporte

Para reportar problemas o sugerencias, contacta al equipo de desarrollo.

---

**Versión:** 2.0.0  
**Última actualización:** 2024

# 🚗 API de Alquiler de Vehículos

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pipenv](https://img.shields.io/badge/pipenv-3775A9?style=for-the-badge&logo=python&logoColor=white)

**API RESTful moderna para gestionar el alquiler de vehículos** 🏍️ 🚲

*Construida con FastAPI y diseñada para simplicidad y escalabilidad*

</div>

---

## Estructura del Proyecto

```
├── main.py                 # Aplicación principal de FastAPI
├── database.py            # Base de datos simulada en memoria
├── requirements.txt       # Dependencias del proyecto
├── models/               # Modelos de datos
│   ├── __init__.py
│   ├── vehiculo.py       # Modelo de vehículos
│   ├── cliente.py        # Modelo de clientes
│   └── alquiler.py       # Modelo de alquileres
├── routes/               # Endpoints de la API
│   ├── __init__.py
│   ├── vehiculos.py      # CRUD de vehículos
│   ├── clientes.py       # CRUD de clientes
│   └── alquileres.py     # Gestión de alquileres
└── services/             # Lógica de negocio
    ├── __init__.py
    └── alquiler_service.py
```

## ✨ Funcionalidades Principales

<table>
<tr>
<td width="50%">

### 🚗 Gestión de Vehículos
- **Tipos soportados**: 
  - 🚗 Autos
  - 🏍️ Motos
  - 🚲 Bicicletas
- **Estados**: Disponible, Alquilado, Mantenimiento
- ✅ CRUD completo con validaciones

### 👥 Gestión de Clientes
- 📝 Registro y actualización de clientes
- 🔍 Validación de duplicados (cédula, email)
- 📊 Historial de alquileres por cliente

</td>
<td width="50%">

### 📅 Gestión de Alquileres
- **🆕 Crear alquiler**: Validación de disponibilidad y cálculo automático de precios
- **🔄 Devolver vehículo**: Cambio de estado y registro de devolución
- **💰 Calcular costos**: Preview de precios con descuentos aplicables
- **❌ Cancelar alquiler**: Liberación del vehículo

### 🎯 Sistema de Descuentos
- 💸 **5%** descuento para alquileres de **3+ días**
- 💸 **15%** descuento para alquileres de **7+ días** (semana completa)
- 🚲 **10%** descuento adicional para bicicletas en alquileres de **5+ días**

</td>
</tr>
</table>

## 😎 Endpoints Principales

### 📚 Ejemplos de Uso

#### 1️⃣ Endpoint con Path Parameter
```http
GET /alquileres/{alquiler_id}
```
🔍 Obtiene detalles completos de un alquiler específico.

#### 2️⃣ Endpoint con Query Parameters
```http
GET /vehiculos/?tipo=auto&disponible=true
GET /alquileres/?estado=activo&cliente_id=1&fecha_desde=2024-01-01
```
🔎 Filtra registros según criterios específicos.

#### 3️⃣ Endpoint POST con Body
```json
POST /alquileres/
{
  "cliente_id": 1,
  "vehiculo_id": 3,
  "fecha_inicio": "2024-09-01",
  "fecha_fin": "2024-09-05",
  "observaciones": "Cliente experimentado"
}
```
➕ Crea un nuevo alquiler con validación automática.

### 📊 Endpoints Disponibles

<details>
<summary>👁️ Ver todos los endpoints</summary>

#### Vehículos
- `GET /vehiculos/` - Listar todos los vehículos
- `POST /vehiculos/` - Crear nuevo vehículo
- `GET /vehiculos/{vehiculo_id}` - Obtener vehículo por ID
- `PUT /vehiculos/{vehiculo_id}` - Actualizar vehículo
- `DELETE /vehiculos/{vehiculo_id}` - Eliminar vehículo

#### Clientes
- `GET /clientes/` - Listar todos los clientes
- `POST /clientes/` - Crear nuevo cliente
- `GET /clientes/{cliente_id}` - Obtener cliente por ID
- `PUT /clientes/{cliente_id}` - Actualizar cliente
- `DELETE /clientes/{cliente_id}` - Eliminar cliente

#### Alquileres
- `GET /alquileres/` - Listar todos los alquileres
- `POST /alquileres/` - Crear nuevo alquiler
- `GET /alquileres/{alquiler_id}` - Obtener alquiler por ID
- `PUT /alquileres/{alquiler_id}/devolver` - Devolver vehículo
- `DELETE /alquileres/{alquiler_id}` - Cancelar alquiler
- `POST /alquileres/calcular-costo` - Calcular costo de alquiler

</details>

## 🚀 Instalación y Ejecución

### 🔧 Prerrequisitos

- Python 3.7+
- Pipenv (recomendado para manejo de dependencias)

### 📦 Opción 1: Con Pipenv (Recomendado)

```bash
# 1. Instalar pipenv si no lo tienes
pip install pipenv

# 2. Crear entorno virtual e instalar dependencias
pipenv install

# 3. Activar el entorno virtual
pipenv shell

# 4. Ejecutar la aplicación
uvicorn main:app --reload
```

### 📦 Opción 2: Con pip tradicional

```bash
# 1. Crear entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar la aplicación
uvicorn main:app --reload
```

### 🌍 Acceder a la API

Una vez ejecutada la aplicación, puedes acceder a:

| Recurso | URL | Descripción |
|---------|-----|-------------|
| 📄 Swagger UI | [http://localhost:8000/docs](http://localhost:8000/docs) | Documentación interactiva |
| 📚 ReDoc | [http://localhost:8000/redoc](http://localhost:8000/redoc) | Documentación alternativa |
| 🗺️ API Base | [http://localhost:8000](http://localhost:8000) | Endpoint raíz |

## 📊 Datos de Ejemplo

La API incluye datos precargados para facilitar las pruebas:

- 🚗 **6 vehículos** (2 autos, 2 motos, 2 bicicletas)
- 👥 **3 clientes** registrados con información completa
- 📅 **1 alquiler activo** de ejemplo

## 🔧 Características Técnicas

- ⚡ **Framework**: FastAPI con validación automática de datos
- 📄 **Documentación**: Generación automática con OpenAPI/Swagger
- ✅ **Validación**: Schemas de Pydantic para requests/responses
- 🏧 **Arquitectura**: Separación clara de responsabilidades (MVC)
- ⚠️ **Manejo de errores**: Respuestas HTTP estándar con mensajes descriptivos
- 💾 **Base de datos**: En memoria (ideal para desarrollo y pruebas)

## 🔍 ¿Por qué usar Pipenv?

Pipenv combina las funcionalidades de pip y virtualenv en una sola herramienta:

✅ **Ventajas de Pipenv:**
- 🛡️ Manejo automático de entornos virtuales
- 🔒 Archivo `Pipfile.lock` para dependencias deterministas
- 📋 Separación entre dependencias de producción y desarrollo
- 🔍 Detección automática de vulnerabilidades con `pipenv check`
- 📈 Mejor rendimiento en instalación de dependencias

## 🚀 Próximos Pasos

<details>
<summary>📈 Mejoras Planificadas</summary>

- [ ] 💾 Integración con base de datos real (PostgreSQL/MySQL)
- [ ] 🔐 Sistema de autenticación y autorización
- [ ] 📧 Notificaciones por email/SMS
- [ ] 📈 Dashboard con estadísticas
- [ ] 📱 API para aplicación móvil
- [ ] 🗺️ Integración con mapas para ubicación de vehículos
- [ ] 🔍 Tests automatizados con pytest
- [ ] 🐳 Dockerización para despliegue

</details>

---

<div align="center">

**¡Listo para alquilar vehículos de forma moderna! 🎆**

*Si tienes preguntas o sugerencias, no dudes en crear un issue* 🚀

</div>
