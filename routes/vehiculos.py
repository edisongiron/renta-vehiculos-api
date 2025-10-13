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
    """
    Endpoint para obtener lista de vehículos con filtros opcionales.
    
    Permite filtrar por tipo (AUTO, MOTO, BICICLETA), estado y disponibilidad.
    Requiere autenticación mediante token JWT.
    
    Args:
        db: Sesión de base de datos
        current_user: Usuario autenticado
        tipo: Tipo de vehículo para filtrar
        estado: Estado del vehículo para filtrar
        disponible: Si es True, solo muestra vehículos disponibles
        
    Returns:
        Lista de vehículos que cumplen con los filtros
    """
    return Vehiculos.obtener_vehiculos(db, tipo, estado, disponible)


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
    """
    Endpoint para obtener un vehículo específico por ID.
    
    Args:
        vehiculo_id: ID único del vehículo
        db: Sesión de base de datos
        current_user: Usuario autenticado
        
    Returns:
        Datos completos del vehículo
    """
    return Vehiculos.obtener_vehiculo(db, vehiculo_id)


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
    """
    Endpoint para crear un nuevo vehículo en la flota.
    
    Valida que la placa no esté duplicada antes de crear.
    
    Args:
        vehiculo_data: Datos del vehículo a crear
        db: Sesión de base de datos
        current_user: Usuario autenticado
        
    Returns:
        Vehículo creado con todos sus datos
    """
    return Vehiculos.crear_vehiculo(db, vehiculo_data)


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
    """
    Endpoint para actualizar datos de un vehículo.
    
    Solo actualiza los campos proporcionados en la petición.
    
    Args:
        vehiculo_id: ID del vehículo a actualizar
        vehiculo_data: Nuevos datos del vehículo
        db: Sesión de base de datos
        current_user: Usuario autenticado
        
    Returns:
        Vehículo actualizado con los cambios aplicados
    """
    return Vehiculos.actualizar_vehiculo(db, vehiculo_id, vehiculo_data)


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
    """
    Endpoint para eliminar un vehículo de la flota.
    
    Verifica que el vehículo no tenga alquileres activos antes de eliminar.
    No se puede eliminar un vehículo que esté actualmente alquilado.
    
    Args:
        vehiculo_id: ID del vehículo a eliminar
        db: Sesión de base de datos
        current_user: Usuario autenticado
        
    Returns:
        Mensaje de confirmación de eliminación
    """
    return Vehiculos.eliminar_vehiculo(db, vehiculo_id)


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
    """
    Endpoint para verificar la disponibilidad de un vehículo.
    
    Consulta si el vehículo tiene alquileres activos y devuelve
    su estado de disponibilidad con la razón si no está disponible.
    
    Args:
        vehiculo_id: ID del vehículo a verificar
        db: Sesión de base de datos
        current_user: Usuario autenticado
        
    Returns:
        Estado de disponibilidad del vehículo con razón si no está disponible
    """
    return Vehiculos.verificar_disponibilidad(db, vehiculo_id)
