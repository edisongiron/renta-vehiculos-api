from fastapi import APIRouter
from controllers.Alquileres.index import Alquileres
from typing import List
from models.alquiler import AlquilerResponse, AlquilerDetallado, CostoResponse


router = APIRouter(prefix="/alquileres", tags=["Alquileres"])


# GET -> /alquileres
router.add_api_route(
    path="/", 
    endpoint=Alquileres.obtener_alquileres, 
    methods=["GET"], 
    response_model=List[AlquilerResponse],
    summary="Obtener todos los alquileres",
    description="Obtiene una lista de todos los alquileres con filtros opcionales" 
)


# GET -> /alquileres/{alquiler_id}
router.add_api_route(
    path="/{alquiler_id}",
    endpoint=Alquileres.obtener_alquiler_detallado,
    response_model=AlquilerDetallado,
    methods=["GET"],
    summary="Obtener alquiler detallado por ID",
    description="Obtiene los detalles completos de un alquiler específico incluyendo información del cliente y vehículo"
)


# POST -> /alquileres
router.add_api_route(
    path="/",
    response_model=AlquilerResponse,
    endpoint=Alquileres.crear_alquiler,
    methods=["POST"], 
    status_code=201,
    summary="Crear nuevo alquiler",
    description="Crea un nuevo alquiler de vehículo. Calcula automáticamente el precio total y valida disponibilidad."
)


# POST -> /calcular-costo
router.add_api_route(
    path="/calcular-costo",
    endpoint=Alquileres.calcular_costo_alquiler,
    response_model=CostoResponse,
    summary="Calcular costo de alquiler",
    description="Calcula el costo total de un alquiler sin crearlo, incluyendo descuentos aplicables",
    methods=["POST"]
)


# PUT -> /alquileres/{alquiler_id}/devolver
router.add_api_route(
    path="/{alquiler_id}/devolver",
    response_model=AlquilerResponse,
    endpoint=Alquileres.devolver_vehiculo,
    summary="Devolver vehículo alquilado",
    description="Registra la devolución de un vehículo y actualiza el estado del alquiler",
    methods=["PUT"]
)


# DELETE -> /alquileres/{alquiler_id}
router.add_api_route(
    path="/{alquiler_id}",
    endpoint=Alquileres.cancelar_alquiler,
    summary="Cancelar alquiler",
    description="Cancela un alquiler activo y libera el vehículo",
    methods=["DELETE"]
)
