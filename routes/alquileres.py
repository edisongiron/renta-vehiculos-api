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
    """
    Endpoint para obtener lista de alquileres con filtros opcionales.
    
    Permite filtrar por estado, cliente, vehículo y rango de fechas.
    Requiere autenticación mediante token JWT.
    
    Args:
        current_user: Usuario autenticado actual
        estado_id: Estado del alquiler (ACTIVO, COMPLETADO, CANCELADO)
        cliente_id: ID del cliente para filtrar
        vehiculo_id: ID del vehículo para filtrar
        fecha_desde: Fecha de inicio del rango (YYYY-MM-DD)
        fecha_hasta: Fecha de fin del rango (YYYY-MM-DD)
        
    Returns:
        Lista de alquileres que cumplen con los filtros
    """
    return Alquileres.obtener_alquileres(
        estado_id=estado_id,
        cliente_id=cliente_id,
        vehiculo_id=vehiculo_id,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
    )


@router.get(
    path="/{alquiler_id}",
    response_model=AlquilerDetallado,
    summary="Obtener alquiler detallado por ID",
    description="Obtiene los detalles completos de un alquiler específico incluyendo información del cliente y vehículo. Requiere autenticación.",
)
def obtener_alquiler_detallado(alquiler_id: str):
    """
    Endpoint para obtener información detallada de un alquiler.
    
    Incluye datos completos del cliente, vehículo y estado del alquiler.
    
    Args:
        alquiler_id: ID único del alquiler a consultar
        
    Returns:
        Información detallada del alquiler con datos de cliente y vehículo
    """
    return Alquileres.obtener_alquiler_detallado(alquiler_id)


@router.post(
    path="/",
    response_model=AlquilerResponse,
    status_code=201,
    summary="Crear nuevo alquiler",
    description="Crea un nuevo alquiler de vehículo. Calcula automáticamente el precio total y valida disponibilidad. Requiere autenticación.",
)
def crear_alquiler(alquiler: AlquilerCreate, db: Session = Depends(get_db)):
    """
    Endpoint para crear un nuevo alquiler.
    
    Valida disponibilidad del vehículo, existencia del cliente
    y calcula automáticamente días y precio total con descuentos.
    
    Args:
        alquiler: Datos del alquiler a crear
        db: Sesión de base de datos
        
    Returns:
        Alquiler creado con todos sus datos calculados
    """
    return Alquileres.crear_alquiler(db, alquiler)


@router.post(
    path="/calcular-costo",
    response_model=CostoResponse,
    summary="Calcular costo de alquiler",
    description="Calcula el costo total de un alquiler sin crearlo, incluyendo descuentos aplicables. Requiere autenticación.",
)
def calcular_costo_alquiler(data: CalcularCosto):
    """
    Endpoint para calcular el costo estimado de un alquiler.
    
    Calcula días, precio base y descuentos sin crear el alquiler.
    Útil para mostrar cotizaciones a los clientes.
    
    Args:
        data: Datos para calcular (vehículo_id, fecha_inicio, fecha_fin)
        
    Returns:
        Desglose completo del costo con descuentos aplicables
    """
    return Alquileres.calcular_costo_alquiler(data)


@router.put(
    path="/{alquiler_id}/devolver",
    response_model=AlquilerResponse,
    summary="Devolver vehículo alquilado",
    description="Registra la devolución de un vehículo y actualiza el estado del alquiler. Requiere autenticación.",
)
def devolver_vehiculo(
    alquiler_id: str, devolucion_data: AlquilerDevolucion, db: Session = Depends(get_db)
):
    """
    Endpoint para registrar la devolución de un vehículo.
    
    Actualiza el estado a COMPLETADO, registra fecha de devolución
    y recalcula el precio si hubo devolución anticipada o tardía.
    
    Args:
        alquiler_id: ID del alquiler a devolver
        devolucion_data: Fecha de devolución y observaciones opcionales
        db: Sesión de base de datos
        
    Returns:
        Alquiler actualizado con estado COMPLETADO
    """
    return Alquileres.devolver_vehiculo(db, alquiler_id, devolucion_data)


@router.delete(
    path="/{alquiler_id}",
    summary="Cancelar alquiler",
    description="Cancela un alquiler activo y libera el vehículo. Requiere autenticación.",
)
def cancelar_alquiler(alquiler_id: str, db: Session = Depends(get_db)):
    """
    Endpoint para cancelar un alquiler activo.
    
    Cambia el estado a CANCELADO y libera el vehículo.
    Solo se pueden cancelar alquileres en estado ACTIVO.
    
    Args:
        alquiler_id: ID del alquiler a cancelar
        db: Sesión de base de datos
        
    Returns:
        Mensaje de confirmación de cancelación
    """
    return Alquileres.cancelar_alquiler(db, alquiler_id)
