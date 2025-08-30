from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from models.alquiler import Alquiler, EstadoAlquiler
from models.vehiculo import EstadoVehiculo
from schemas.alquiler_schemas import (
    AlquilerCreate, AlquilerDevolucion, AlquilerResponse,
    AlquilerDetallado, CalcularCosto, CostoResponse
)
from database import alquileres_db, vehiculos_db, clientes_db
from services.alquiler_service import (
    calcular_dias_alquiler, calcular_precio_total,
    verificar_disponibilidad_vehiculo, verificar_cliente_existe, obtener_siguiente_id
)
from datetime import datetime

router = APIRouter(prefix="/alquileres", tags=["Alquileres"])


@router.get(
    "/",
    response_model=List[AlquilerResponse],
    summary="Obtener todos los alquileres",
    description="Obtiene una lista de todos los alquileres con filtros opcionales"
)
def obtener_alquileres(
    estado: Optional[EstadoAlquiler] = Query(
        None, description="Filtrar por estado del alquiler"),
    cliente_id: Optional[int] = Query(
        None, description="Filtrar por ID del cliente"),
    vehiculo_id: Optional[int] = Query(
        None, description="Filtrar por ID del vehículo"),
    fecha_desde: Optional[str] = Query(
        None, description="Filtrar desde esta fecha (YYYY-MM-DD)"),
    fecha_hasta: Optional[str] = Query(
        None, description="Filtrar hasta esta fecha (YYYY-MM-DD)")
) -> List[AlquilerResponse]:
    alquileres = alquileres_db.copy()

    if estado:
        alquileres = [a for a in alquileres if a.estado == estado]

    if cliente_id:
        alquileres = [a for a in alquileres if a.cliente_id == cliente_id]

    if vehiculo_id:
        alquileres = [a for a in alquileres if a.vehiculo_id == vehiculo_id]

    if fecha_desde:
        try:
            fecha_desde_dt = datetime.strptime(fecha_desde, "%Y-%m-%d").date()
            alquileres = [
                a for a in alquileres
                if datetime.strptime(a.fecha_inicio, "%Y-%m-%d").date() >= fecha_desde_dt
            ]
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Formato de fecha_desde inválido (use YYYY-MM-DD)")

    if fecha_hasta:
        try:
            fecha_hasta_dt = datetime.strptime(fecha_hasta, "%Y-%m-%d").date()
            alquileres = [
                a for a in alquileres
                if datetime.strptime(a.fecha_inicio, "%Y-%m-%d").date() <= fecha_hasta_dt
            ]
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Formato de fecha_hasta inválido (use YYYY-MM-DD)")

    return [AlquilerResponse.model_validate(a.model_dump()) for a in alquileres]


@router.get(
    "/{alquiler_id}",
    response_model=AlquilerDetallado,
    summary="Obtener alquiler detallado por ID",
    description="Obtiene los detalles completos de un alquiler específico incluyendo información del cliente y vehículo"
)
def obtener_alquiler_detallado(alquiler_id: int) -> AlquilerDetallado:
    alquiler = next((a for a in alquileres_db if a.id == alquiler_id), None)
    
    if not alquiler:
        raise HTTPException(status_code=404, detail="Alquiler no encontrado")

    cliente = next((c for c in clientes_db if c.id ==
                   alquiler.cliente_id), None)
    vehiculo = next((v for v in vehiculos_db if v.id ==
                    alquiler.vehiculo_id), None)

    if not cliente or not vehiculo:
        raise HTTPException(
            status_code=500, detail="Error: datos inconsistentes en el alquiler")

    return AlquilerDetallado(
        id=alquiler.id,
        cliente_nombre=cliente.nombre,
        cliente_email=cliente.email,
        vehiculo_marca=vehiculo.marca,
        vehiculo_modelo=vehiculo.modelo,
        vehiculo_placa=vehiculo.placa,
        vehiculo_tipo=vehiculo.tipo,
        fecha_inicio=alquiler.fecha_inicio,
        fecha_fin=alquiler.fecha_fin,
        dias_alquiler=alquiler.dias_alquiler,
        precio_total=alquiler.precio_total,
        estado=alquiler.estado,
        fecha_devolucion_real=alquiler.fecha_devolucion_real,
        observaciones=alquiler.observaciones
    )


@router.post(
    "/",
    response_model=AlquilerResponse,
    status_code=201,
    summary="Crear nuevo alquiler",
    description="Crea un nuevo alquiler de vehículo. Calcula automáticamente el precio total y valida disponibilidad."
)
def crear_alquiler(alquiler_data: AlquilerCreate) -> AlquilerResponse:
    # Verificar que el cliente existe
    if not verificar_cliente_existe(alquiler_data.cliente_id):
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # Verificar disponibilidad del vehículo
    disponible, razon = verificar_disponibilidad_vehiculo(
        alquiler_data.vehiculo_id,
        alquiler_data.fecha_inicio,
        alquiler_data.fecha_fin
    )

    if not disponible:
        raise HTTPException(status_code=400, detail=razon)

    # Calcular días y precio
    dias = calcular_dias_alquiler(
        alquiler_data.fecha_inicio, alquiler_data.fecha_fin)
    precio_total, _, _ = calcular_precio_total(alquiler_data.vehiculo_id, dias)

    # Crear el alquiler
    nuevo_id = obtener_siguiente_id("alquiler")
    nuevo_alquiler = Alquiler(
        id=nuevo_id,
        dias_alquiler=dias,
        precio_total=precio_total,
        **alquiler_data.model_dump()
    )

    alquileres_db.append(nuevo_alquiler)

    # Actualizar estado del vehículo
    for vehiculo in vehiculos_db:
        if vehiculo.id == alquiler_data.vehiculo_id:
            vehiculo.estado = EstadoVehiculo.ALQUILADO
            break

    return AlquilerResponse.model_validate(nuevo_alquiler.model_dump())


@router.post(
    "/calcular-costo",
    response_model=CostoResponse,
    summary="Calcular costo de alquiler",
    description="Calcula el costo total de un alquiler sin crearlo, incluyendo descuentos aplicables"
)
def calcular_costo_alquiler(calculo_data: CalcularCosto) -> CostoResponse:
    vehiculo = next((v for v in vehiculos_db if v.id ==
                    calculo_data.vehiculo_id), None)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    dias = calcular_dias_alquiler(
        calculo_data.fecha_inicio, calculo_data.fecha_fin)
    precio_total, descuento_aplicado, razon_descuento = calcular_precio_total(
        calculo_data.vehiculo_id, dias)

    return CostoResponse(
        vehiculo_id=calculo_data.vehiculo_id,
        precio_por_dia=vehiculo.precio_por_dia,
        dias_alquiler=dias,
        precio_total=precio_total,
        descuento_aplicado=descuento_aplicado,
        razon_descuento=razon_descuento
    )


@router.put(
    "/{alquiler_id}/devolver",
    response_model=AlquilerResponse,
    summary="Devolver vehículo alquilado",
    description="Registra la devolución de un vehículo y actualiza el estado del alquiler"
)
def devolver_vehiculo(alquiler_id: int, devolucion_data: AlquilerDevolucion) -> AlquilerResponse:
    alquiler = next((a for a in alquileres_db if a.id == alquiler_id), None)
    if not alquiler:
        raise HTTPException(status_code=404, detail="Alquiler no encontrado")

    if alquiler.estado != EstadoAlquiler.ACTIVO:
        raise HTTPException(
            status_code=400, detail="El alquiler no está activo")

    # Validar fecha de devolución
    try:
        fecha_devolucion = datetime.strptime(
            devolucion_data.fecha_devolucion, "%Y-%m-%d").date()
        fecha_inicio = datetime.strptime(
            alquiler.fecha_inicio, "%Y-%m-%d").date()

        if fecha_devolucion < fecha_inicio:
            raise HTTPException(
                status_code=400,
                detail="La fecha de devolución no puede ser anterior al inicio del alquiler"
            )
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Formato de fecha inválido (use YYYY-MM-DD)")

    # Actualizar alquiler
    for index, a in enumerate(alquileres_db):
        if a.id == alquiler_id:
            alquileres_db[index].estado = EstadoAlquiler.COMPLETADO
            alquileres_db[index].fecha_devolucion_real = devolucion_data.fecha_devolucion
            if devolucion_data.observaciones:
                alquileres_db[index].observaciones = devolucion_data.observaciones

            # Actualizar estado del vehículo
            for vehiculo in vehiculos_db:
                if vehiculo.id == alquiler.vehiculo_id:
                    vehiculo.estado = EstadoVehiculo.DISPONIBLE
                    break

            return AlquilerResponse.model_validate(alquileres_db[index].model_dump())

    raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.delete(
    "/{alquiler_id}",
    summary="Cancelar alquiler",
    description="Cancela un alquiler activo y libera el vehículo"
)
def cancelar_alquiler(alquiler_id: int):
    alquiler = next((a for a in alquileres_db if a.id == alquiler_id), None)
    if not alquiler:
        raise HTTPException(status_code=404, detail="Alquiler no encontrado")

    if alquiler.estado != EstadoAlquiler.ACTIVO:
        raise HTTPException(
            status_code=400, detail="Solo se pueden cancelar alquileres activos")

    # Actualizar estado del alquiler
    for index, a in enumerate(alquileres_db):
        if a.id == alquiler_id:
            alquileres_db[index].estado = EstadoAlquiler.CANCELADO

            # Liberar el vehículo
            for vehiculo in vehiculos_db:
                if vehiculo.id == alquiler.vehiculo_id:
                    vehiculo.estado = EstadoVehiculo.DISPONIBLE
                    break

            return {"message": "Alquiler cancelado exitosamente"}

    raise HTTPException(status_code=500, detail="Error interno del servidor")
