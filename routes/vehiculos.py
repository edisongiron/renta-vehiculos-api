from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from controllers.Vehiculos.index import Vehiculos
from models.Vehiculo import Vehiculo, TipoVehiculo, EstadoVehiculo, VehiculoCreate, VehiculoUpdate, VehiculoResponse, VehiculoDisponibilidad


router = APIRouter(prefix="/vehiculos", tags=["Vehículos"])


# GET -> /
router.add_api_route(
    "/",
    response_model=List[VehiculoResponse],
    endpoint=Vehiculos.obtener_vehiculos,
    summary="Obtener todos los vehículos",
    description="Obtiene una lista de todos los vehículos con filtros opcionales",
    methods=["GET"]
)


# GET -> /{vehiculo_id}
router.add_api_route(
    "/{vehiculo_id}",
    response_model=VehiculoResponse,
    endpoint=Vehiculos.obtener_vehiculo,
    summary="Obtener vehículo por ID",
    description="Obtiene los detalles de un vehículo específico por su ID",
    methods=["GET"]
)


# POST -> /
router.add_api_route(
    "/",
    response_model=VehiculoResponse,
    endpoint=Vehiculos.crear_vehiculo,
    status_code=201,
    summary="Crear nuevo vehículo",
    description="Registra un nuevo vehículo en la flota",
    methods=["POST"]
)


# PUT -> /{vehiculo_id}
router.add_api_route(
    "/{vehiculo_id}",
    response_model=VehiculoResponse,
    endpoint=Vehiculos.actualizar_vehiculo,
    summary="Actualizar vehículo",
    description="Actualiza los datos de un vehículo existente",
    methods=["PUT"]
)


# DELETE -> /{vehiculo_id}
router.add_api_route(
    "/{vehiculo_id}",
    summary="Eliminar vehículo",
    endpoint=Vehiculos.eliminar_vehiculo,
    description="Elimina un vehículo de la flota (solo si no tiene alquileres activos)",
    methods=["DELETE"]
)


# GET -> /{vehiculo_id}/disponibilidad
router.add_api_route(
    "/{vehiculo_id}/disponibilidad",
    response_model=VehiculoDisponibilidad,
    endpoint=Vehiculos.verificar_disponibilidad,
    summary="Verificar disponibilidad de vehículo",
    description="Verifica si un vehículo está disponible para alquiler",
    methods=["GET"]
)

