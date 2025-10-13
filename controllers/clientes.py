from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from fastapi import Query, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from schemas.clientes import cliente as clientes
from schemas.alquileres import alquileres as alquileres
from sqlalchemy import select, insert, update, delete
from datetime import datetime


class Clientes:
    """
    Controlador para gestionar las operaciones de clientes.
    
    Esta clase maneja todas las operaciones CRUD relacionadas con clientes,
    incluyendo búsqueda, creación, actualización y eliminación con validaciones.
    """

    @staticmethod
    def obtener_clientes(
        db: Session,
        buscar: Optional[str] = Query(None, description="Buscar por nombre o email"),
    ) -> List[ClienteResponse]:
        """
        Obtiene una lista de clientes con búsqueda opcional.
        
        Permite filtrar clientes por nombre o email mediante búsqueda de texto.
        
        Args:
            db: Sesión de base de datos SQLAlchemy
            buscar: Texto para buscar en nombre o email del cliente
            
        Returns:
            Lista de objetos ClienteResponse con los clientes encontrados
        """
        query = select(clientes)

        if buscar:
            buscar_lower = buscar.lower()
            query = query.where(
                (clientes.c.nombre.ilike(f"%{buscar_lower}%"))
                | (clientes.c.email.ilike(f"%{buscar_lower}%"))
            )

        result = db.execute(query).fetchall()
        return [ClienteResponse(**dict(row._mapping)) for row in result]

    @staticmethod
    def obtener_cliente(db: Session, cedula: int) -> ClienteResponse:
        """
        Obtiene un cliente específico por su cédula.
        
        Args:
            db: Sesión de base de datos SQLAlchemy
            cedula: Número de cédula del cliente a buscar
            
        Returns:
            Objeto ClienteResponse con los datos del cliente
            
        Raises:
            HTTPException: Si el cliente no existe
        """
        query = select(clientes).where(clientes.c.cedula == cedula)
        result = db.execute(query).fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        return ClienteResponse(**dict(result._mapping))

    @staticmethod
    def crear_cliente(db: Session, cliente_data: ClienteCreate) -> ClienteResponse:
        """
        Crea un nuevo cliente en el sistema.
        
        Valida que la cédula y el email no estén duplicados antes de crear.
        La fecha de registro se asigna automáticamente.
        
        Args:
            db: Sesión de base de datos SQLAlchemy
            cliente_data: Datos del cliente a crear
            
        Returns:
            Objeto ClienteResponse con el cliente creado
            
        Raises:
            HTTPException: Si la cédula o email ya están registrados
        """
        cedula_query = select(clientes).where(clientes.c.cedula == cliente_data.cedula)
        cedula_result = db.execute(cedula_query).fetchone()

        if cedula_result:
            raise HTTPException(status_code=400, detail="La cédula ya está registrada")

        email_query = select(clientes).where(clientes.c.email == cliente_data.email)
        email_result = db.execute(email_query).fetchone()

        if email_result:
            raise HTTPException(status_code=400, detail="El email ya está registrado")

        data_dict = cliente_data.model_dump()
        data_dict["fecha_registro"] = datetime.now().strftime("%Y-%m-%d")

        insert_query = insert(clientes).values(**data_dict)
        result = db.execute(insert_query)
        db.commit()

        nuevo_id = result.inserted_primary_key[0]
        query = select(clientes).where(clientes.c.id == nuevo_id)
        nuevo_cliente = db.execute(query).fetchone()

        return ClienteResponse(**dict(nuevo_cliente._mapping))

    @staticmethod
    def actualizar_cliente(
        db: Session, cedula: int, cliente_data: ClienteUpdate
    ) -> ClienteResponse:
        """
        Actualiza los datos de un cliente existente.
        
        Valida que el email no esté duplicado si se está actualizando.
        Solo actualiza los campos proporcionados.
        
        Args:
            db: Sesión de base de datos SQLAlchemy
            cedula: Cédula del cliente a actualizar
            cliente_data: Nuevos datos del cliente (solo campos a actualizar)
            
        Returns:
            Objeto ClienteResponse con el cliente actualizado
            
        Raises:
            HTTPException: Si el cliente no existe o el email está duplicado
        """
        query = select(clientes).where(clientes.c.cedula == cedula)
        result = db.execute(query).fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        update_data = cliente_data.model_dump(exclude_unset=True)
        if "email" in update_data and update_data["email"] != result.email:
            email_query = select(clientes).where(
                clientes.c.email == update_data["email"]
            )
            email_result = db.execute(email_query).fetchone()

            if email_result:
                raise HTTPException(
                    status_code=400, detail="El email ya está registrado"
                )

        if update_data:
            update_query = (
                update(clientes)
                .where(clientes.c.cedula == cedula)
                .values(**update_data)
            )
            db.execute(update_query)
            db.commit()

        updated_query = select(clientes).where(clientes.c.cedula == cedula)
        updated_cliente = db.execute(updated_query).fetchone()

        if not updated_cliente:
            raise HTTPException(status_code=500, detail="Error al actualizar el cliente")

        return ClienteResponse(**dict(updated_cliente._mapping))

    @staticmethod
    def eliminar_cliente(db: Session, cedula: str):
        """
        Elimina un cliente del sistema.
        
        Verifica que el cliente no tenga alquileres activos antes de eliminar.
        No se puede eliminar un cliente con alquileres en curso.
        
        Args:
            db: Sesión de base de datos SQLAlchemy
            cedula: Cédula del cliente a eliminar
            
        Returns:
            JSONResponse con mensaje de confirmación
            
        Raises:
            HTTPException: Si el cliente no existe o tiene alquileres activos
        """
        query = select(clientes).where(clientes.c.cedula == cedula)
        existing_cliente = db.execute(query).fetchone()

        if not existing_cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        cliente_id = existing_cliente._mapping["id"]

        from models.alquiler import EstadoAlquiler

        alquiler_query = select(alquileres).where(
            (alquileres.c.cliente_id == cliente_id)
            & (alquileres.c.estado_id == EstadoAlquiler.ACTIVO.value)
        )
        alquiler_activo = db.execute(alquiler_query).fetchone()

        if alquiler_activo:
            raise HTTPException(
                status_code=400,
                detail="No se puede eliminar un cliente con alquileres activos",
            )

        delete_query = delete(clientes).where(clientes.c.id == cliente_id)
        db.execute(delete_query)
        db.commit()

        json = jsonable_encoder({"message": "Cliente eliminado exitosamente"})

        return JSONResponse(status_code=200, content=json)
