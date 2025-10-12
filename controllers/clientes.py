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

    @staticmethod
    def obtener_clientes(
        db: Session,
        buscar: Optional[str] = Query(None, description="Buscar por nombre o email"),
    ) -> List[ClienteResponse]:
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
        query = select(clientes).where(clientes.c.cedula == cedula)
        result = db.execute(query).fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        return ClienteResponse(**dict(result._mapping))

    @staticmethod
    def crear_cliente(db: Session, cliente_data: ClienteCreate) -> ClienteResponse:
        # Verificar que la cédula no esté duplicada
        cedula_query = select(clientes).where(clientes.c.cedula == cliente_data.cedula)
        cedula_result = db.execute(cedula_query).fetchone()

        if cedula_result:
            raise HTTPException(status_code=400, detail="La cédula ya está registrada")

        # Verificar que el email no esté duplicado
        email_query = select(clientes).where(clientes.c.email == cliente_data.email)
        email_result = db.execute(email_query).fetchone()

        if email_result:
            raise HTTPException(status_code=400, detail="El email ya está registrado")

        # Insertar nuevo cliente
        data_dict = cliente_data.model_dump()
        data_dict["fecha_registro"] = datetime.now().strftime("%Y-%m-%d")

        insert_query = insert(clientes).values(**data_dict)
        result = db.execute(insert_query)
        db.commit()

        # Obtener el cliente creado
        nuevo_id = result.inserted_primary_key[0]
        query = select(clientes).where(clientes.c.id == nuevo_id)
        nuevo_cliente = db.execute(query).fetchone()

        return ClienteResponse(**dict(nuevo_cliente._mapping))

    @staticmethod
    def actualizar_cliente(
        db: Session, cedula: int, cliente_data: ClienteUpdate
    ) -> ClienteResponse:
        # Verificar que el cliente existe
        query = select(clientes).where(clientes.c.cedula == cedula)
        result = db.execute(query).fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        # Verificar email duplicado si se está actualizando
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

        # Actualizar solo los campos proporcionados
        if update_data:
            update_query = (
                update(clientes)
                .where(clientes.c.cedula == cedula)
                .values(**update_data)
            )
            db.execute(update_query)
            db.commit()

        # Obtener el cliente actualizado
        updated_query = select(clientes).where(clientes.c.cedula == cedula)
        updated_cliente = db.execute(updated_query).fetchone()

        return ClienteResponse(**dict(updated_cliente._mapping))

    @staticmethod
    def eliminar_cliente(db: Session, cedula: str):
        # Verificar que el cliente existe
        query = select(clientes).where(clientes.c.cedula == cedula)
        existing_cliente = db.execute(query).fetchone()

        if not existing_cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        cliente_id = existing_cliente._mapping["id"]

        # Verificar que el cliente no tenga alquileres activos
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

        # Eliminar el cliente
        delete_query = delete(clientes).where(clientes.c.id == cliente_id)
        db.execute(delete_query)
        db.commit()

        json = jsonable_encoder({"message": "Cliente eliminado exitosamente"})

        return JSONResponse(status_code=200, content=json)
