from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from models.cliente import Cliente
from schemas.cliente_schemas import ClienteCreate, ClienteUpdate, ClienteResponse
from database import clientes_db
from datetime import datetime

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.get(
    "/",
    response_model=List[ClienteResponse],
    summary="Obtener todos los clientes",
    description="Obtiene una lista de todos los clientes registrados"
)
def obtener_clientes(
    buscar: Optional[str] = Query(None, description="Buscar por nombre o email")
) -> List[ClienteResponse]:
    clientes = clientes_db.copy()
    
    if buscar:
        buscar_lower = buscar.lower()
        clientes = [
            c for c in clientes 
            if buscar_lower in c.nombre.lower() or buscar_lower in c.email.lower()
        ]
    
    return [ClienteResponse.model_validate(c.model_dump()) for c in clientes]


@router.get(
    "/{cliente_id}",
    response_model=ClienteResponse,
    summary="Obtener cliente por ID",
    description="Obtiene los detalles de un cliente específico por su ID"
)
def obtener_cliente(cliente_id: int) -> ClienteResponse:
    cliente = next((c for c in clientes_db if c.id == cliente_id), None)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    return ClienteResponse.model_validate(cliente.model_dump())


@router.post(
    "/",
    response_model=ClienteResponse,
    status_code=201,
    summary="Crear nuevo cliente",
    description="Registra un nuevo cliente en el sistema"
)


@router.put(
    "/{cliente_id}",
    response_model=ClienteResponse,
    summary="Actualizar cliente",
    description="Actualiza los datos de un cliente existente"
)
def actualizar_cliente(cliente_id: int, cliente_data: ClienteUpdate) -> ClienteResponse:
    for index, cliente in enumerate(clientes_db):
        if cliente.id == cliente_id:
            # Verificar email duplicado si se está actualizando
            if cliente_data.email and cliente_data.email != cliente.email:
                if any(c.email == cliente_data.email for c in clientes_db):
                    raise HTTPException(status_code=400, detail="El email ya está registrado")
            
            # Actualizar solo los campos proporcionados
            update_data = cliente_data.model_dump(exclude_unset=True)
            updated_cliente = cliente.model_copy(update=update_data)
            clientes_db[index] = updated_cliente
            
            return ClienteResponse.model_validate(updated_cliente.model_dump())
    
    raise HTTPException(status_code=404, detail="Cliente no encontrado")


@router.delete(
    "/{cliente_id}",
    summary="Eliminar cliente",
    description="Elimina un cliente del sistema (solo si no tiene alquileres activos)"
)
def eliminar_cliente(cliente_id: int):
    # Verificar que el cliente no tenga alquileres activos
    from database import alquileres_db
    
    for index, cliente in enumerate(clientes_db):
        if cliente.id == cliente_id:
            del clientes_db[index]
            return {"message": "Cliente eliminado exitosamente"}
    
    raise HTTPException(status_code=404, detail="Cliente no encontrado")
