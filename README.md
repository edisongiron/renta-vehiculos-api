# API de Alquiler de Vehículos

API RESTful para gestionar el alquiler de vehículos (autos, motos y bicicletas) construida con FastAPI.

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
├── schemas/              # Schemas de validación
│   ├── __init__.py
│   ├── vehiculo_schemas.py
│   ├── cliente_schemas.py
│   └── alquiler_schemas.py
├── routes/               # Endpoints de la API
│   ├── __init__.py
│   ├── vehiculos.py      # CRUD de vehículos
│   ├── clientes.py       # CRUD de clientes
│   └── alquileres.py     # Gestión de alquileres
└── services/             # Lógica de negocio
    ├── __init__.py
    └── alquiler_service.py
```

## Funcionalidades Principales

### Gestión de Vehículos
- **Tipos soportados**: Autos, Motos, Bicicletas
- **Estados**: Disponible, Alquilado, Mantenimiento
- CRUD completo con validaciones

### Gestión de Clientes
- Registro y actualización de clientes
- Validación de duplicados (cédula, email)

### Gestión de Alquileres
- **Crear alquiler**: Validación de disponibilidad y cálculo automático de precios
- **Devolver vehículo**: Cambio de estado y registro de devolución
- **Calcular costos**: Preview de precios con descuentos aplicables
- **Cancelar alquiler**: Liberación del vehículo

### Sistema de Descuentos
- 5% descuento para alquileres de 3+ días
- 15% descuento para alquileres de 7+ días (semana completa)
- 10% descuento adicional para bicicletas en alquileres de 5+ días

## Endpoints Principales

### Ejemplos de Uso

#### 1. Endpoint con Path Parameter
```
GET /alquileres/{alquiler_id}
```
Obtiene detalles completos de un alquiler específico.

#### 2. Endpoint con Query Parameters
```
GET /vehiculos/?tipo=auto&disponible=true
GET /alquileres/?estado=activo&cliente_id=1&fecha_desde=2024-01-01
```

#### 3. Endpoint POST con Body
```
POST /alquileres/
{
  "cliente_id": 1,
  "vehiculo_id": 3,
  "fecha_inicio": "2024-09-01",
  "fecha_fin": "2024-09-05",
  "observaciones": "Cliente experimentado"
}
```

## Instalación y Ejecución

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar la aplicación:
```bash
uvicorn main:app --reload
```

3. Acceder a la documentación interactiva:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Datos de Ejemplo

La API incluye datos precargados:
- 6 vehículos (2 autos, 2 motos, 2 bicicletas)
- 3 clientes registrados
- 1 alquiler activo de ejemplo

## Características Técnicas

- **Framework**: FastAPI con validación automática de datos
- **Documentación**: Generación automática con OpenAPI/Swagger
- **Validación**: Schemas de Pydantic para requests/responses
- **Arquitectura**: Separación clara de responsabilidades (MVC)
- **Manejo de errores**: Respuestas HTTP estándar con mensajes descriptivos
