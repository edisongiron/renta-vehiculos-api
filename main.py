from fastapi import FastAPI
from routes.vehiculos import router as vehiculos_router

# Configuración de la aplicación FastAPI
app = FastAPI(
    title="API de Alquiler de Vehículos",
    description="Sistema de gestión para alquiler de autos, motos y bicicletas. "
                "Incluye funcionalidades para gestionar vehículos, clientes y alquileres "
                "con cálculo automático de costos y descuentos.",
    version="1.0.0",
    contact={
        "name": "Soporte API Alquiler",
        "email": "soporte@alquilervehiculos.com"
    }
)

# Registro de routers
app.include_router(vehiculos_router)

@app.get(
    "/",
    summary="Información de la API",
    description="Endpoint raíz que proporciona información básica sobre la API",
    tags=["General"]
)
def root():
    return {
        "message": "Bienvenido a la API de Alquiler de Vehículos",
        "version": "1.0.0",
        "descripcion": "Sistema para gestión de alquiler de autos, motos y bicicletas",
    }



