from fastapi import APIRouter, Depends
from typing import List, Optional

from fastapi.params import Query
from controllers.clientes import Clientes
from models.cliente import ClienteResponse
from utils.auth_utils import get_current_user
from database.db import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/clientes", tags=["Clientes"])


# GET -> /
@router.get(
    path="/",
    response_model=List[ClienteResponse],
    summary="Obtener todos los clientes",
    description="Obtiene una lista de todos los clientes registrados. Requiere autenticación.",
)
def obtener_clientes(
    db: Session = Depends(get_db),
    buscar: Optional[str] = Query(None, description="Buscar por nombre o email"),
):
    return Clientes.obtener_clientes(db, buscar)


# GET -> /{cedula}
@router.get(
    path="/{cedula}",
    response_model=ClienteResponse,
    summary="Obtener cliente por cédula",
    description="Obtiene los detalles de un cliente específico por su cédula. Requiere autenticación.",
)
def obtener_cliente(cedula: str, db: Session = Depends(get_db)):
    return Clientes.obtener_cliente(db, cedula)


# POST -> /
@router.post(
    path="/",
    response_model=ClienteResponse,
    status_code=201,
    summary="Crear nuevo cliente",
    description="Registra un nuevo cliente en el sistema. Requiere autenticación.",
)
def crear_cliente(cliente_data: ClienteResponse, db: Session = Depends(get_db)):
    return Clientes.crear_cliente(db, cliente_data)


# PUT -> /{cedula}
@router.put(
    path="/{cedula}",
    response_model=ClienteResponse,
    summary="Actualizar cliente",
    description="Actualiza los datos de un cliente existente. Requiere autenticación.",
)
def actualizar_cliente(
    cedula: int,
    cliente: ClienteResponse,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return Clientes.actualizar_cliente(db, cedula, cliente)


# DELETE -> /{cliente_id}
@router.delete(
    path="/{cedula}",
    summary="Eliminar cliente",
    description="Elimina un cliente del sistema (solo si no tiene alquileres activos). Requiere autenticación.",
)
def eliminar_cliente(
    cedula: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return Clientes.eliminar_cliente(db, cedula)
