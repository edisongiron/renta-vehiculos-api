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
