from datetime import datetime, date
from typing import Optional
from models.vehiculo import EstadoVehiculo, TipoVehiculo
from models.alquiler import EstadoAlquiler
import database
from database import vehiculos_db, clientes_db, alquileres_db
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

    vehiculo = next((v for v in vehiculos_db if v.id == vehiculo_id), None)
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
    if vehiculo.tipo == TipoVehiculo.BICICLETA and dias >= 5:
        descuento += 0.10  # 10% adicional para bicicletas
        razon_descuento = f"{razon_descuento} + Descuento adicional para bicicletas (10%)"
    
    precio_descuento = precio_base * descuento
    precio_final = precio_base - precio_descuento
    
    return precio_final, precio_descuento if descuento > 0 else None, razon_descuento


def verificar_disponibilidad_vehiculo(vehiculo_id: int, fecha_inicio: str, fecha_fin: str) -> tuple[bool, Optional[str]]:
    """Verifica si un vehículo está disponible para las fechas especificadas"""

    vehiculo = next((v for v in vehiculos_db if v.id == vehiculo_id), None)
    if not vehiculo:
        return False, "Vehículo no encontrado"
    
    if vehiculo.estado != EstadoVehiculo.DISPONIBLE:
        return False, f"Vehículo no disponible - Estado: {vehiculo.estado}"
    
    # Verificar conflictos con alquileres existentes
    inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
    fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
    
    for alquiler in alquileres_db:
        if alquiler.vehiculo_id == vehiculo_id and alquiler.estado == EstadoAlquiler.ACTIVO:
            alquiler_inicio = datetime.strptime(alquiler.fecha_inicio, "%Y-%m-%d").date()
            alquiler_fin = datetime.strptime(alquiler.fecha_fin, "%Y-%m-%d").date()
            
            # Verificar si hay solapamiento de fechas
            if not (fin <= alquiler_inicio or inicio >= alquiler_fin):
                return False, "Vehículo ya está alquilado en esas fechas"
    
    return True, None


def verificar_cliente_existe(cliente_id: int) -> bool:
    """Verifica si un cliente existe en la base de datos"""

    return any(c.id == cliente_id for c in clientes_db)


def obtener_siguiente_id(tabla: str) -> int:
    """Obtiene el siguiente ID disponible para una tabla"""

    if tabla == "vehiculo":
        id_actual = database.next_vehiculo_id
        database.next_vehiculo_id += 1
        return id_actual
    
    elif tabla == "cliente":
        id_actual = database.next_cliente_id
        database.next_cliente_id += 1
        return id_actual
    
    elif tabla == "alquiler":
        id_actual = database.next_alquiler_id
        database.next_alquiler_id += 1
        return id_actual
    
    else:
        raise ValueError(f"Tabla no reconocida: {tabla}")
