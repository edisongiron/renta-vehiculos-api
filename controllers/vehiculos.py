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
    """
    Controlador para gestionar las operaciones de vehículos.
    
    Esta clase maneja todas las operaciones CRUD relacionadas con vehículos,
    incluyendo consulta, creación, actualización, eliminación y verificación de disponibilidad.
    """

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
        """
        Obtiene una lista de vehículos con filtros opcionales.
        
        Permite filtrar por tipo de vehículo (auto, moto, bicicleta),
        estado y disponibilidad.
        
        Args:
            db: Sesión de base de datos SQLAlchemy
            tipo: Tipo de vehículo para filtrar (AUTO, MOTO, BICICLETA)
            estado: Estado del vehículo para filtrar
            disponible: Si es True, filtra solo vehículos disponibles
            
        Returns:
            Lista de objetos VehiculoResponse con los vehículos encontrados
        """
        query = select(vehiculos)

        if tipo:
            query = query.where(vehiculos.c.tipo == tipo.value)

        result = db.execute(query).fetchall()
        return [VehiculoResponse(**dict(row._mapping)) for row in result]

    @staticmethod
    def obtener_vehiculo(db: Session, vehiculo_id: str) -> VehiculoResponse:
        """
        Obtiene un vehículo específico por su ID.
        
        Args:
            db: Sesión de base de datos SQLAlchemy
            vehiculo_id: ID único del vehículo a buscar
            
        Returns:
            Objeto VehiculoResponse con los datos del vehículo
            
        Raises:
            HTTPException: Si el vehículo no existe
        """
        query = select(vehiculos).where(vehiculos.c.id == vehiculo_id)
        result = db.execute(query).fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")

        return VehiculoResponse(**dict(result._mapping))

    @staticmethod
    def crear_vehiculo(db: Session, vehiculo_data: VehiculoCreate) -> VehiculoResponse:
        """
        Crea un nuevo vehículo en la flota.
        
        Valida que la placa del vehículo no esté duplicada antes de crear.
        
        Args:
            db: Sesión de base de datos SQLAlchemy
            vehiculo_data: Datos del vehículo a crear
            
        Returns:
            Objeto VehiculoResponse con el vehículo creado
            
        Raises:
            HTTPException: Si la placa ya está registrada
        """
        existing_query = select(vehiculos).where(
            vehiculos.c.placa == vehiculo_data.placa
        )
        existing_result = db.execute(existing_query).fetchone()

        if existing_result:
            raise HTTPException(status_code=400, detail="La placa ya está registrada")

        insert_query = insert(vehiculos).values(**vehiculo_data.model_dump())
        result = db.execute(insert_query)
        db.commit()

        nuevo_id = result.inserted_primary_key[0]
        query = select(vehiculos).where(vehiculos.c.id == nuevo_id)
        nuevo_vehiculo = db.execute(query).fetchone()

        return VehiculoResponse(**dict(nuevo_vehiculo._mapping))

    @staticmethod
    def actualizar_vehiculo(
        db: Session, vehiculo_id: str, vehiculo_data: VehiculoUpdate
    ) -> VehiculoResponse:
        """
        Actualiza los datos de un vehículo existente.
        
        Solo actualiza los campos proporcionados en la petición.
        
        Args:
            db: Sesión de base de datos SQLAlchemy
            vehiculo_id: ID del vehículo a actualizar
            vehiculo_data: Nuevos datos del vehículo (solo campos a actualizar)
            
        Returns:
            Objeto VehiculoResponse con el vehículo actualizado
            
        Raises:
            HTTPException: Si el vehículo no existe
        """
        query = select(vehiculos).where(vehiculos.c.id == vehiculo_id)
        existing_vehiculo = db.execute(query).fetchone()

        if not existing_vehiculo:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")

        update_data = vehiculo_data.model_dump(exclude_unset=True)
        if update_data:
            update_query = (
                update(vehiculos)
                .where(vehiculos.c.id == vehiculo_id)
                .values(**update_data)
            )
            db.execute(update_query)
            db.commit()

        updated_query = select(vehiculos).where(vehiculos.c.id == vehiculo_id)
        updated_vehiculo = db.execute(updated_query).fetchone()

        return VehiculoResponse(**dict(updated_vehiculo._mapping))

    @staticmethod
    def eliminar_vehiculo(db: Session, vehiculo_id: str):
        """
        Elimina un vehículo de la flota.
        
        Verifica que el vehículo no tenga alquileres activos antes de eliminar.
        No se puede eliminar un vehículo que esté actualmente alquilado.
        
        Args:
            db: Sesión de base de datos SQLAlchemy
            vehiculo_id: ID del vehículo a eliminar
            
        Returns:
            Diccionario con mensaje de confirmación
            
        Raises:
            HTTPException: Si el vehículo no existe o tiene alquileres activos
        """
        query = select(vehiculos).where(vehiculos.c.id == vehiculo_id)
        existing_vehiculo = db.execute(query).fetchone()

        if not existing_vehiculo:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")

        alquiler_query = select(alquileres).where(
            (alquileres.c.vehiculo_id == vehiculo_id)
            & (alquileres.c.estado_id == 1)
        )
        alquiler_activo = db.execute(alquiler_query).fetchone()

        if alquiler_activo:
            raise HTTPException(
                status_code=400,
                detail="No se puede eliminar un vehículo con alquileres activos",
            )

        delete_query = delete(vehiculos).where(vehiculos.c.id == vehiculo_id)
        db.execute(delete_query)
        db.commit()

        return {"message": "Vehículo eliminado exitosamente"}

    @staticmethod
    def verificar_disponibilidad(
        db: Session, vehiculo_id: str
    ) -> VehiculoDisponibilidad:
        """
        Verifica la disponibilidad de un vehículo para alquiler.
        
        Determina si el vehículo está disponible consultando si tiene
        alquileres activos en el momento actual.
        
        Args:
            db: Sesión de base de datos SQLAlchemy
            vehiculo_id: ID del vehículo a verificar
            
        Returns:
            Objeto VehiculoDisponibilidad con estado de disponibilidad y razón
            
        Raises:
            HTTPException: Si el vehículo no existe
        """
        vehiculo_query = select(vehiculos).where(vehiculos.c.id == vehiculo_id)
        vehiculo = db.execute(vehiculo_query).fetchone()

        if not vehiculo:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")

        alquiler_query = select(alquileres).where(
            (alquileres.c.vehiculo_id == vehiculo_id)
            & (alquileres.c.estado_id == 1)
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
