from datetime import datetime
from typing import Optional
from models.Vehiculo import EstadoVehiculo, TipoVehiculo
from models.alquiler import EstadoAlquiler
from database.db import conn
from schemas.vehiculo import vehiculo as ve
from schemas.clientes import cliente as cl
from schemas.alquileres import alquileres as alq
from sqlalchemy import select
from fastapi import HTTPException


def calcular_dias_alquiler(fecha_inicio: str, fecha_fin: str) -> int:
    """Calcula el número de días entre dos fechas"""
    
    try:
        inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
        
        if fin <= inicio:
            raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio")
        
        return (fin - inicio).days
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Error en las fechas: {str(e)}")


def calcular_precio_total(vehiculo_id: int, dias: int) -> tuple[float, Optional[float], Optional[str]]:
    """Calcula el precio total del alquiler con posibles descuentos"""

    query = select(ve).where(ve.c.id == vehiculo_id)
    vehiculo = conn.execute(query).fetchone()
    
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    
    precio_base = vehiculo.precio_por_dia * dias
    descuento = 0.0
    razon_descuento = None
    
    # Aplicar descuentos por días
    if dias >= 7:
        descuento = 0.15  # 15% de descuento por semana completa
        razon_descuento = "Descuento por alquiler semanal (15%)"
        
    elif dias >= 3:
        descuento = 0.05  # 5% de descuento por 3 o más días
        razon_descuento = "Descuento por alquiler de 3+ días (5%)"
    
    # Descuento adicional para bicicletas en alquileres largos
    if vehiculo.tipo == TipoVehiculo.BICICLETA.value and dias >= 5:
        descuento += 0.10  # 10% adicional para bicicletas
        razon_descuento = f"{razon_descuento} + Descuento adicional para bicicletas (10%)"
    
    precio_descuento = precio_base * descuento
    precio_final = precio_base - precio_descuento
    
    return precio_final, precio_descuento if descuento > 0 else None, razon_descuento


def verificar_disponibilidad_vehiculo(
    vehiculo_id: int, fecha_inicio: str, fecha_fin: str
) -> tuple[bool, Optional[str]]:
    """Verifica si un vehículo está disponible para las fechas especificadas"""

    # Verificar que el vehículo exista
    query = select(ve).where(ve.c.id == vehiculo_id)
    vehiculo = conn.execute(query).fetchone()

    if not vehiculo:
        return False, "Vehículo no encontrado"

    # Convertir fechas
    inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
    fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()

    # Buscar alquileres activos de este vehículo
    alquileres_query = select(alq).where(
        (alq.c.vehiculo_id == vehiculo_id) &
        (alq.c.estado_id == EstadoAlquiler.ACTIVO.value)
    )
    alquileres = conn.execute(alquileres_query).fetchall()

    # Verificar solapamientos de fechas
    for alquiler in alquileres:
        alquiler_inicio = datetime.strptime(alquiler.fecha_inicio, "%Y-%m-%d").date()
        alquiler_fin = datetime.strptime(alquiler.fecha_fin, "%Y-%m-%d").date()

        if not (fin <= alquiler_inicio or inicio >= alquiler_fin):
            return False, "Vehículo ya está alquilado en esas fechas"

    return True, None


def verificar_cliente_existe(id: int) -> bool:
    """Verifica si un cliente existe en la base de datos"""

    query = select(cl).where(cl.c.id == id)
    result = conn.execute(query).fetchone()
    return result is not None


# This function is no longer needed since we use autoincrement in the database
# IDs are handled automatically by SQLAlchemy
