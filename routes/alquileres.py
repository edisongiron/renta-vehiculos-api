from fastapi import APIRouter, Query, Depends
from controllers.alquileres import Alquileres
from typing import List, Optional
from models.alquiler import (
    AlquilerResponse,
    AlquilerDetallado,
    CostoResponse,
    AlquilerCreate,
    AlquilerDevolucion,
    CalcularCosto,
    EstadoAlquiler,
)
from utils.auth_utils import get_current_user
from database.db import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/alquileres", tags=["Alquileres"])


# GET -> /alquileres
@router.get(
    path="/",
    response_model=List[AlquilerResponse],
    summary="Obtener todos los alquileres",
    description="Obtiene una lista de todos los alquileres con filtros opcionales. Requiere autenticación.",
)
def obtener_alquileres(
    current_user: dict = Depends(get_current_user),
    estado_id: Optional[EstadoAlquiler] = Query(
        None, description="Filtrar por estado del alquiler"
    ),
    cliente_id: Optional[int] = Query(None, description="Filtrar por ID del cliente"),
    vehiculo_id: Optional[int] = Query(None, description="Filtrar por ID del vehículo"),
    fecha_desde: Optional[str] = Query(
        None, description="Filtrar desde esta fecha (YYYY-MM-DD)"
    ),
    fecha_hasta: Optional[str] = Query(
        None, description="Filtrar hasta esta fecha (YYYY-MM-DD)"
    ),
):
    return Alquileres.obtener_alquileres(
        estado_id=estado_id,
        cliente_id=cliente_id,
        vehiculo_id=vehiculo_id,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
    )


# GET -> /alquileres/{alquiler_id}
@router.get(
    path="/{alquiler_id}",
    response_model=AlquilerDetallado,
    summary="Obtener alquiler detallado por ID",
    description="Obtiene los detalles completos de un alquiler específico incluyendo información del cliente y vehículo. Requiere autenticación.",
)
def obtener_alquiler_detallado(alquiler_id: str):
    return Alquileres.obtener_alquiler_detallado(alquiler_id)


# POST -> /alquileres
@router.post(
    path="/",
    response_model=AlquilerResponse,
    status_code=201,
    summary="Crear nuevo alquiler",
    description="Crea un nuevo alquiler de vehículo. Calcula automáticamente el precio total y valida disponibilidad. Requiere autenticación.",
)
def crear_alquiler(alquiler: AlquilerCreate, db: Session = Depends(get_db)):

    return Alquileres.crear_alquiler(db, alquiler)


# POST -> /calcular-costo
@router.post(
    path="/calcular-costo",
    response_model=CostoResponse,
    summary="Calcular costo de alquiler",
    description="Calcula el costo total de un alquiler sin crearlo, incluyendo descuentos aplicables. Requiere autenticación.",
)
def calcular_costo_alquiler(data: CalcularCosto):
    return Alquileres.calcular_costo_alquiler(data)


# PUT -> /alquileres/{alquiler_id}/devolver
@router.put(
    path="/{alquiler_id}/devolver",
    response_model=AlquilerResponse,
    summary="Devolver vehículo alquilado",
    description="Registra la devolución de un vehículo y actualiza el estado del alquiler. Requiere autenticación.",
)
def devolver_vehiculo(
    alquiler_id: str, devolucion_data: AlquilerDevolucion, db: Session = Depends(get_db)
):
    return Alquileres.devolver_vehiculo(db, alquiler_id, devolucion_data)


# DELETE -> /alquileres/{alquiler_id}
@router.delete(
    path="/{alquiler_id}",
    summary="Cancelar alquiler",
    description="Cancela un alquiler activo y libera el vehículo. Requiere autenticación.",
)
def cancelar_alquiler(alquiler_id: str, db: Session = Depends(get_db)):
    return Alquileres.cancelar_alquiler(db, alquiler_id)
