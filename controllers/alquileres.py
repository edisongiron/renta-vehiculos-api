from fastapi import Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from utils.alquiler_utils import (
    calcular_dias_alquiler,
    calcular_precio_total,
    verificar_disponibilidad_vehiculo,
    verificar_cliente_existe,
)

from database.db import conn
from schemas.alquileres import alquileres
from schemas.vehiculo import vehiculo as vehiculos
from schemas.clientes import cliente as clientes
from sqlalchemy import select, insert, update

from models.alquiler import (
    EstadoAlquiler,
    AlquilerCreate,
    AlquilerDevolucion,
    AlquilerResponse,
    AlquilerDetallado,
    CalcularCosto,
    CostoResponse,
)

class Alquileres:

    # GET -> /alquileres
    @staticmethod
    def obtener_alquileres(
        estado_id: Optional[EstadoAlquiler] = Query(
            None, description="Filtrar por estado del alquiler"
        ),
        cliente_id: Optional[int] = Query(
            None, description="Filtrar por ID del cliente"
        ),
        vehiculo_id: Optional[int] = Query(
            None, description="Filtrar por ID del vehículo"
        ),
        fecha_desde: Optional[str] = Query(
            None, description="Filtrar desde esta fecha (YYYY-MM-DD)"
        ),
        fecha_hasta: Optional[str] = Query(
            None, description="Filtrar hasta esta fecha (YYYY-MM-DD)"
        ),
    ) -> List[AlquilerResponse]:
        query = select(alquileres)

        if estado_id:
            query = query.where(alquileres.c.estado_id == estado_id.value)

        if cliente_id:
            query = query.where(alquileres.c.cliente_id == cliente_id)

        if vehiculo_id:
            query = query.where(alquileres.c.vehiculo_id == vehiculo_id)

        if fecha_desde:
            try:
                datetime.strptime(fecha_desde, "%Y-%m-%d")
                query = query.where(alquileres.c.fecha_inicio >= fecha_desde)
            
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Formato de fecha_desde inválido (use YYYY-MM-DD)",
                )

        if fecha_hasta:
            try:
                datetime.strptime(fecha_hasta, "%Y-%m-%d")
                query = query.where(alquileres.c.fecha_inicio <= fecha_hasta)

            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Formato de fecha_hasta inválido (use YYYY-MM-DD)",
                )

        result = conn.execute(query).fetchall()
        return [AlquilerResponse(**dict(row._mapping)) for row in result]

    # GET -> /alquileres/{alquiler_id}
    @staticmethod
    def obtener_alquiler_detallado(alquiler_id: str) -> AlquilerDetallado:
        # Obtener el alquiler
        alquiler_query = select(alquileres).where(alquileres.c.id == alquiler_id)
        alquiler = conn.execute(alquiler_query).fetchone()

        if not alquiler:
            raise HTTPException(status_code=404, detail="Alquiler no encontrado")

        # Obtener el cliente
        cliente_query = select(clientes).where(clientes.c.id == alquiler.cliente_id)
        cliente = conn.execute(cliente_query).fetchone()

        # Obtener el vehículo
        vehiculo_query = select(vehiculos).where(vehiculos.c.id == alquiler.vehiculo_id)
        vehiculo = conn.execute(vehiculo_query).fetchone()

        if not cliente or not vehiculo:
            raise HTTPException(
                status_code=500, detail="Error: datos inconsistentes en el alquiler"
            )

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
            estado_id=alquiler.estado_id,
            fecha_devolucion_real=alquiler.fecha_devolucion_real,
            observaciones=alquiler.observaciones,
        )

    # POST -> /alquileres
    @staticmethod
    def crear_alquiler(db: Session, alquiler_data: AlquilerCreate) -> AlquilerResponse:
        # Verificar que el cliente existe
        if not verificar_cliente_existe(alquiler_data.cliente_id):
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        # Verificar disponibilidad del vehículo en el rango de fechas
        disponible, razon = verificar_disponibilidad_vehiculo(
            alquiler_data.vehiculo_id,
            alquiler_data.fecha_inicio,
            alquiler_data.fecha_fin,
        )

        if not disponible:
            raise HTTPException(status_code=400, detail=razon)

        # Calcular días y precio
        dias = calcular_dias_alquiler(
            alquiler_data.fecha_inicio, alquiler_data.fecha_fin
        )

        precio_total, descuento_aplicado, razon_descuento = calcular_precio_total(
            alquiler_data.vehiculo_id, dias
        )

        # Preparar datos para insertar (sin fecha_creacion)
        data_dict = alquiler_data.model_dump()
        data_dict["dias_alquiler"] = dias
        data_dict["precio_total"] = precio_total
        data_dict["estado_id"] = EstadoAlquiler.ACTIVO.value
        data_dict["fecha_devolucion_real"] = None

        insert_query = insert(alquileres).values(**data_dict)
        result = db.execute(insert_query)

        last_id = (
            result.inserted_primary_key[0] if result.inserted_primary_key else None
        )
        
        db.commit()

        # Si no lo logró, buscar el último ID como fallback
        if not last_id:
            query_last = (
                select(alquileres.c.id).order_by(alquileres.c.id.desc()).limit(1)
            )
            
            last_row = db.execute(query_last).fetchone()
            last_id = last_row[0] if last_row else None

        query = select(alquileres).where(alquileres.c.id == last_id)
        nuevo_alquiler = db.execute(query).fetchone()

        if not nuevo_alquiler:
            raise HTTPException(status_code=500, detail="Error al crear el alquiler")

        return AlquilerResponse(**dict(nuevo_alquiler._mapping))

    # POST -> /calcular-costo
    @staticmethod
    def calcular_costo_alquiler(calculo_data: CalcularCosto) -> CostoResponse:
        # Obtener vehículo (necesitamos precio_por_dia para la respuesta)
        vehiculo_q = select(vehiculos).where(vehiculos.c.id == calculo_data.vehiculo_id)
        vehiculo_row = conn.execute(vehiculo_q).fetchone()
        
        if not vehiculo_row:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")

        # Calcular días y costo usando tus utilidades
        dias = calcular_dias_alquiler(calculo_data.fecha_inicio, calculo_data.fecha_fin)
        precio_total, descuento_aplicado, razon_descuento = calcular_precio_total(
            calculo_data.vehiculo_id, dias
        )

        # Construir respuesta
        return CostoResponse(
            vehiculo_id=calculo_data.vehiculo_id,
            precio_por_dia=vehiculo_row.precio_por_dia,
            dias_alquiler=dias,
            precio_total=precio_total,
            descuento_aplicado=descuento_aplicado,
            razon_descuento=razon_descuento,
        )

    # PUT -> /alquileres/{alquiler_id}/devolver
    @staticmethod
    def devolver_vehiculo(
        db: Session, alquiler_id: str, devolucion_data: AlquilerDevolucion
    ) -> AlquilerResponse:
        
        # Obtener alquiler
        alquiler_q = select(alquileres).where(alquileres.c.id == alquiler_id)
        alquiler = conn.execute(alquiler_q).fetchone()
        
        if not alquiler:
            raise HTTPException(status_code=404, detail="Alquiler no encontrado")

        if alquiler.estado_id != EstadoAlquiler.ACTIVO.value:
            raise HTTPException(status_code=400, detail="El alquiler no está activo")

        # Validar fecha de devolución
        try:
            fecha_devolucion = datetime.strptime(
                devolucion_data.fecha_devolucion, "%Y-%m-%d"
            ).date()

            fecha_inicio = datetime.strptime(alquiler.fecha_inicio, "%Y-%m-%d").date()
            if fecha_devolucion < fecha_inicio:
                raise HTTPException(
                    status_code=400,
                    detail="La fecha de devolución no puede ser anterior al inicio del alquiler",
                )
        
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Formato de fecha inválido (use YYYY-MM-DD)"
            )

        # Recalcular días y, si deseas, precio final (por si devolvieron antes o después)
        dias_actualizados = calcular_dias_alquiler(
            alquiler.fecha_inicio, devolucion_data.fecha_devolucion
        )
        precio_total, descuento_aplicado, razon_descuento = calcular_precio_total(
            alquiler.vehiculo_id, dias_actualizados
        )

        # Actualizar alquiler en BD
        update_data = {
            "estado_id": EstadoAlquiler.COMPLETADO.value,
            "fecha_devolucion_real": devolucion_data.fecha_devolucion,
            "dias_alquiler": dias_actualizados,
            "precio_total": precio_total,
        }

        if devolucion_data.observaciones:
            update_data["observaciones"] = devolucion_data.observaciones

        update_query = (
            update(alquileres)
            .where(alquileres.c.id == alquiler_id)
            .values(**update_data)
        )

        db.execute(update_query)
        db.commit()

        # Obtener alquiler actualizado y devolver
        updated_q = select(alquileres).where(alquileres.c.id == alquiler_id)
        updated = db.execute(updated_q).fetchone()
        
        if not updated:
            raise HTTPException(
                status_code=500, detail="Error al actualizar el alquiler"
            )

        return AlquilerResponse(**dict(updated._mapping))

    # DELETE -> /alquileres/{alquiler_id}
    @staticmethod
    def cancelar_alquiler(db: Session, alquiler_id: str) -> JSONResponse:
        
        alquiler_q = select(alquileres).where(alquileres.c.id == alquiler_id)
        alquiler = db.execute(alquiler_q).fetchone()
        
        if not alquiler:
            raise HTTPException(status_code=404, detail="Alquiler no encontrado")

        if alquiler.estado_id != EstadoAlquiler.ACTIVO.value:
            raise HTTPException(
                status_code=400, detail="Solo se pueden cancelar alquileres activos"
            )

        # Actualizar estado del alquiler a CANCELADO
        update_query = (
            update(alquileres)
            .where(alquileres.c.id == alquiler_id)
            .values(estado_id=EstadoAlquiler.CANCELADO.value)
        )
        
        db.execute(update_query)
        db.commit()

        json = jsonable_encoder({"message": "Alquiler cancelado exitosamente"})
        return JSONResponse(status_code=200, content=json)
