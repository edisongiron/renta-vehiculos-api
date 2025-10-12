from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from routes.vehiculos import router as vehiculos_router
from routes.clientes import router as clientes_router
from routes.alquileres import router as alquileres_router
from routes.auth import router as auth_router


# Configuración de la aplicación FastAPI
app = FastAPI(
    title="API de Alquiler de Vehículos",
    description="Sistema de gestión para alquiler de autos, motos y bicicletas. "
    "Incluye funcionalidades para gestionar vehículos, clientes y alquileres "
    "con cálculo automático de costos y descuentos.",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de routers
app.include_router(auth_router)
app.include_router(vehiculos_router)
app.include_router(clientes_router)
app.include_router(alquileres_router)

@app.get(
    "/",
    summary="Información de la API",
    description="Endpoint raíz que proporciona información básica sobre la API",
    tags=["General"],
)
def root():
    return {
        "message": "Bienvenido a la API de Alquiler de Vehículos",
        "version": "1.0.0",
        "descripcion": "Sistema para gestión de alquiler de autos, motos y bicicletas",
    }

if __name__ == "__main__":
    # Para desarrollo local seguro, usar solo localhost
    # Cambia a "0.0.0.0" si necesitas acceso desde otras IPs
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="info")


