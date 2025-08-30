from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from models.vehiculo import Vehiculo, TipoVehiculo, EstadoVehiculo
from schemas.vehiculo_schemas import VehiculoCreate, VehiculoUpdate, VehiculoResponse, VehiculoDisponibilidad
from database import vehiculos_db


router = APIRouter(prefix="/vehiculos", tags=["Vehículos"])


@router.get(
    "/",
    response_model=List[VehiculoResponse],
    summary="Obtener todos los vehículos",
    description="Obtiene una lista de todos los vehículos con filtros opcionales"
)
def obtener_vehiculos(
    tipo: Optional[TipoVehiculo] = Query(None, description="Filtrar por tipo de vehículo"),
    estado: Optional[EstadoVehiculo] = Query(None, description="Filtrar por estado del vehículo"),
    disponible: Optional[bool] = Query(None, description="Filtrar solo vehículos disponibles")
) -> List[VehiculoResponse]:
    vehiculos = vehiculos_db.copy()
    
    if tipo:
        vehiculos = [v for v in vehiculos if v.tipo == tipo]
    
    if estado:
        vehiculos = [v for v in vehiculos if v.estado == estado]
    
    if disponible is not None:
        if disponible:
            vehiculos = [v for v in vehiculos if v.estado == EstadoVehiculo.DISPONIBLE]
        else:
            vehiculos = [v for v in vehiculos if v.estado != EstadoVehiculo.DISPONIBLE]
    
    return [VehiculoResponse.model_validate(v.model_dump()) for v in vehiculos]


@router.get(
    "/{vehiculo_id}",
    response_model=VehiculoResponse,
    summary="Obtener vehículo por ID",
    description="Obtiene los detalles de un vehículo específico por su ID"
)
def obtener_vehiculo(vehiculo_id: int) -> VehiculoResponse:
    vehiculo = next((v for v in vehiculos_db if v.id == vehiculo_id), None)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    
    return VehiculoResponse.model_validate(vehiculo.model_dump())


@router.post(
    "/",
    response_model=VehiculoResponse,
    status_code=201,
    summary="Crear nuevo vehículo",
    description="Registra un nuevo vehículo en la flota"
)
def crear_vehiculo(vehiculo_data: VehiculoCreate) -> VehiculoResponse:
    # Verificar que la placa no esté duplicada
    if any(v.placa == vehiculo_data.placa for v in vehiculos_db):
        raise HTTPException(status_code=400, detail="La placa ya está registrada")
    
    nuevo_id = obtener_siguiente_id("vehiculo")
    nuevo_vehiculo = Vehiculo(
        id=nuevo_id,
        **vehiculo_data.model_dump()
    )
    
    vehiculos_db.append(nuevo_vehiculo)
    return VehiculoResponse.model_validate(nuevo_vehiculo.model_dump())


@router.put(
    "/{vehiculo_id}",
    response_model=VehiculoResponse,
    summary="Actualizar vehículo",
    description="Actualiza los datos de un vehículo existente"
)
def actualizar_vehiculo(vehiculo_id: int, vehiculo_data: VehiculoUpdate) -> VehiculoResponse:
    for index, vehiculo in enumerate(vehiculos_db):
        if vehiculo.id == vehiculo_id:
            # Actualizar solo los campos proporcionados
            update_data = vehiculo_data.model_dump(exclude_unset=True)
            updated_vehiculo = vehiculo.model_copy(update=update_data)
            vehiculos_db[index] = updated_vehiculo
            
            return VehiculoResponse.model_validate(updated_vehiculo.model_dump())
    
    raise HTTPException(status_code=404, detail="Vehículo no encontrado")


@router.delete(
    "/{vehiculo_id}",
    summary="Eliminar vehículo",
    description="Elimina un vehículo de la flota (solo si no tiene alquileres activos)"
)
def eliminar_vehiculo(vehiculo_id: int):
    # Verificar que el vehículo no tenga alquileres activos
    from database import alquileres_db
    from models.alquiler import EstadoAlquiler
    
    alquiler_activo = any(
        a.vehiculo_id == vehiculo_id and a.estado == EstadoAlquiler.ACTIVO 
        for a in alquileres_db
    )
    
    if alquiler_activo:
        raise HTTPException(
            status_code=400, 
            detail="No se puede eliminar un vehículo con alquileres activos"
        )
    
    for index, vehiculo in enumerate(vehiculos_db):
        if vehiculo.id == vehiculo_id:
            del vehiculos_db[index]
            return {"message": "Vehículo eliminado exitosamente"}
    
    raise HTTPException(status_code=404, detail="Vehículo no encontrado")


@router.get(
    "/{vehiculo_id}/disponibilidad",
    response_model=VehiculoDisponibilidad,
    summary="Verificar disponibilidad de vehículo",
    description="Verifica si un vehículo está disponible para alquiler"
)
def verificar_disponibilidad(vehiculo_id: int) -> VehiculoDisponibilidad:
    vehiculo = next((v for v in vehiculos_db if v.id == vehiculo_id), None)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    
    disponible = vehiculo.estado == EstadoVehiculo.DISPONIBLE
    razon = None if disponible else f"Estado actual: {vehiculo.estado}"
    
    return VehiculoDisponibilidad(
        vehiculo_id=vehiculo_id,
        disponible=disponible,
        razon=razon
    )
