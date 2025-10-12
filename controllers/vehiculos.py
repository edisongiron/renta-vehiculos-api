from fastapi import Query, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from models.Vehiculo import (
    Vehiculo,
    TipoVehiculo,
    EstadoVehiculo,
    VehiculoCreate,
    VehiculoUpdate,
    VehiculoResponse,
    VehiculoDisponibilidad,
)
from schemas.vehiculo import vehiculo as vehiculos
from schemas.alquileres import alquileres
from sqlalchemy import select, insert, update, delete


class Vehiculos:

    @staticmethod
    def obtener_vehiculos(
        db: Session,
        tipo: Optional[TipoVehiculo] = Query(
            None, description="Filtrar por tipo de vehículo"
        ),
        estado: Optional[EstadoVehiculo] = Query(
            None, description="Filtrar por estado del vehículo"
        ),
        disponible: Optional[bool] = Query(
            None, description="Filtrar solo vehículos disponibles"
        ),
    ) -> List[VehiculoResponse]:

        query = select(vehiculos)

        if tipo:
            query = query.where(vehiculos.c.tipo == tipo.value)

        # Nota: Los filtros de estado y disponible están relacionados con alquileres,
        # no con el vehículo directamente. Por ahora, solo filtramos por tipo.
        # Para implementar correctamente se necesitaría un JOIN con alquileres

        result = db.execute(query).fetchall()
        return [VehiculoResponse(**dict(row._mapping)) for row in result]

    @staticmethod
    def obtener_vehiculo(db: Session, vehiculo_id: str) -> VehiculoResponse:
        query = select(vehiculos).where(vehiculos.c.id == vehiculo_id)
        result = db.execute(query).fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")

        return VehiculoResponse(**dict(result._mapping))

    @staticmethod
    def crear_vehiculo(db: Session, vehiculo_data: VehiculoCreate) -> VehiculoResponse:
        # Verificar que la placa no esté duplicada
        existing_query = select(vehiculos).where(
            vehiculos.c.placa == vehiculo_data.placa
        )
        existing_result = db.execute(existing_query).fetchone()

        if existing_result:
            raise HTTPException(status_code=400, detail="La placa ya está registrada")

        # Insertar nuevo vehículo
        insert_query = insert(vehiculos).values(**vehiculo_data.model_dump())
        result = db.execute(insert_query)
        db.commit()

        # Obtener el vehículo creado
        nuevo_id = result.inserted_primary_key[0]
        query = select(vehiculos).where(vehiculos.c.id == nuevo_id)
        nuevo_vehiculo = db.execute(query).fetchone()

        return VehiculoResponse(**dict(nuevo_vehiculo._mapping))

    @staticmethod
    def actualizar_vehiculo(
        db: Session, vehiculo_id: str, vehiculo_data: VehiculoUpdate
    ) -> VehiculoResponse:
        # Verificar que el vehículo existe
        query = select(vehiculos).where(vehiculos.c.id == vehiculo_id)
        existing_vehiculo = db.execute(query).fetchone()

        if not existing_vehiculo:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")

        # Actualizar solo los campos proporcionados
        update_data = vehiculo_data.model_dump(exclude_unset=True)
        if update_data:
            update_query = (
                update(vehiculos)
                .where(vehiculos.c.id == vehiculo_id)
                .values(**update_data)
            )
            db.execute(update_query)
            db.commit()

        # Obtener el vehículo actualizado
        updated_query = select(vehiculos).where(vehiculos.c.id == vehiculo_id)
        updated_vehiculo = db.execute(updated_query).fetchone()

        return VehiculoResponse(**dict(updated_vehiculo._mapping))

    @staticmethod
    def eliminar_vehiculo(db: Session, vehiculo_id: str):
        # Verificar que el vehículo existe
        query = select(vehiculos).where(vehiculos.c.id == vehiculo_id)
        existing_vehiculo = db.execute(query).fetchone()

        if not existing_vehiculo:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")

        # Verificar que el vehículo no tenga alquileres activos (estado_id = 1 es "activo")
        alquiler_query = select(alquileres).where(
            (alquileres.c.vehiculo_id == vehiculo_id)
            & (alquileres.c.estado_id == 1)  # 1 = activo
        )
        alquiler_activo = db.execute(alquiler_query).fetchone()

        if alquiler_activo:
            raise HTTPException(
                status_code=400,
                detail="No se puede eliminar un vehículo con alquileres activos",
            )

        # Eliminar el vehículo
        delete_query = delete(vehiculos).where(vehiculos.c.id == vehiculo_id)
        db.execute(delete_query)
        db.commit()

        return {"message": "Vehículo eliminado exitosamente"}

    @staticmethod
    def verificar_disponibilidad(
        db: Session, vehiculo_id: str
    ) -> VehiculoDisponibilidad:
        # Primero verificar que el vehículo existe
        vehiculo_query = select(vehiculos).where(vehiculos.c.id == vehiculo_id)
        vehiculo = db.execute(vehiculo_query).fetchone()

        if not vehiculo:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")

        # Verificar si tiene alquileres activos (estado_id = 1)
        alquiler_query = select(alquileres).where(
            (alquileres.c.vehiculo_id == vehiculo_id)
            & (alquileres.c.estado_id == 1)  # 1 = activo
        )
        alquiler_activo = db.execute(alquiler_query).fetchone()

        if alquiler_activo:
            return VehiculoDisponibilidad(
                vehiculo_id=vehiculo_id,
                disponible=False,
                razon="El vehículo tiene un alquiler activo",
            )
        else:
            return VehiculoDisponibilidad(
                vehiculo_id=vehiculo_id, disponible=True, razon=None
            )
