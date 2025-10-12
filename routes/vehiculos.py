from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from controllers.vehiculos import Vehiculos
from models.Vehiculo import (
    VehiculoResponse,
    VehiculoDisponibilidad,
    VehiculoCreate,
    VehiculoUpdate,
    TipoVehiculo,
    EstadoVehiculo,
)
from database.db import get_db
from sqlalchemy.orm import Session
from utils.auth_utils import get_current_user


router = APIRouter(prefix="/vehiculos", tags=["Vehículos"])


# GET -> /
@router.get(
    "/",
    response_model=List[VehiculoResponse],
    summary="Obtener todos los vehículos",
    description="Obtiene una lista de todos los vehículos con filtros opcionales. Requiere autenticación.",
)
def obtener_vehiculos(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    tipo: Optional[TipoVehiculo] = Query(
        None, description="Filtrar por tipo de vehículo"
    ),
    estado: Optional[EstadoVehiculo] = Query(
        None, description="Filtrar por estado del vehículo"
    ),
    disponible: Optional[bool] = Query(
        None, description="Filtrar solo vehículos disponibles"
    ),
):
    return Vehiculos.obtener_vehiculos(db, tipo, estado, disponible)


# GET -> /{vehiculo_id}
@router.get(
    "/{vehiculo_id}",
    response_model=VehiculoResponse,
    summary="Obtener vehículo por ID",
    description="Obtiene los detalles de un vehículo específico por su ID. Requiere autenticación.",
)
def obtener_vehiculo(
    vehiculo_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return Vehiculos.obtener_vehiculo(db, vehiculo_id)


# POST -> /
@router.post(
    "/",
    response_model=VehiculoResponse,
    status_code=201,
    summary="Crear nuevo vehículo",
    description="Registra un nuevo vehículo en la flota. Requiere autenticación.",
)
def crear_vehiculo(
    vehiculo_data: VehiculoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return Vehiculos.crear_vehiculo(db, vehiculo_data)


# PUT -> /{vehiculo_id}
@router.put(
    "/{vehiculo_id}",
    response_model=VehiculoResponse,
    summary="Actualizar vehículo",
    description="Actualiza los datos de un vehículo existente. Requiere autenticación.",
)
def actualizar_vehiculo(
    vehiculo_id: str,
    vehiculo_data: VehiculoUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return Vehiculos.actualizar_vehiculo(db, vehiculo_id, vehiculo_data)


# DELETE -> /{vehiculo_id}
@router.delete(
    "/{vehiculo_id}",
    summary="Eliminar vehículo",
    description="Elimina un vehículo de la flota (solo si no tiene alquileres activos). Requiere autenticación.",
)
def eliminar_vehiculo(
    vehiculo_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return Vehiculos.eliminar_vehiculo(db, vehiculo_id)


# GET -> /{vehiculo_id}/disponibilidad
@router.get(
    "/{vehiculo_id}/disponibilidad",
    response_model=VehiculoDisponibilidad,
    summary="Verificar disponibilidad de vehículo",
    description="Verifica si un vehículo está disponible para alquiler. Requiere autenticación.",
)
def verificar_disponibilidad(
    vehiculo_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return Vehiculos.verificar_disponibilidad(db, vehiculo_id)
