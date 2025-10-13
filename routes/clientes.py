from fastapi import APIRouter, Depends
from typing import List, Optional

from fastapi.params import Query
from controllers.clientes import Clientes
from models.cliente import ClienteResponse
from utils.auth_utils import get_current_user
from database.db import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/clientes", tags=["Clientes"])


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
    """
    Endpoint para obtener lista de clientes con búsqueda opcional.
    
    Permite buscar clientes por nombre o email mediante texto libre.
    Requiere autenticación mediante token JWT.
    
    Args:
        db: Sesión de base de datos
        buscar: Texto para buscar en nombre o email
        
    Returns:
        Lista de clientes que coinciden con la búsqueda
    """
    return Clientes.obtener_clientes(db, buscar)


@router.get(
    path="/{cedula}",
    response_model=ClienteResponse,
    summary="Obtener cliente por cédula",
    description="Obtiene los detalles de un cliente específico por su cédula. Requiere autenticación.",
)
def obtener_cliente(cedula: str, db: Session = Depends(get_db)):
    """
    Endpoint para obtener un cliente específico por cédula.
    
    Args:
        cedula: Número de cédula del cliente
        db: Sesión de base de datos
        
    Returns:
        Datos completos del cliente
    """
    return Clientes.obtener_cliente(db, cedula)


@router.post(
    path="/",
    response_model=ClienteResponse,
    status_code=201,
    summary="Crear nuevo cliente",
    description="Registra un nuevo cliente en el sistema. Requiere autenticación.",
)
def crear_cliente(cliente_data: ClienteResponse, db: Session = Depends(get_db)):
    """
    Endpoint para crear un nuevo cliente.
    
    Valida que la cédula y email no estén duplicados.
    Asigna automáticamente la fecha de registro.
    
    Args:
        cliente_data: Datos del cliente a crear
        db: Sesión de base de datos
        
    Returns:
        Cliente creado con todos sus datos
    """
    return Clientes.crear_cliente(db, cliente_data)


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
    """
    Endpoint para actualizar datos de un cliente.
    
    Solo actualiza los campos proporcionados en la petición.
    Valida que el nuevo email no esté duplicado.
    
    Args:
        cedula: Cédula del cliente a actualizar
        cliente: Nuevos datos del cliente
        current_user: Usuario autenticado
        db: Sesión de base de datos
        
    Returns:
        Cliente actualizado con los cambios aplicados
    """
    return Clientes.actualizar_cliente(db, cedula, cliente)


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
    """
    Endpoint para eliminar un cliente.
    
    Verifica que el cliente no tenga alquileres activos antes de eliminar.
    No se puede eliminar un cliente con alquileres en curso.
    
    Args:
        cedula: Cédula del cliente a eliminar
        current_user: Usuario autenticado
        db: Sesión de base de datos
        
    Returns:
        Mensaje de confirmación de eliminación
    """
    return Clientes.eliminar_cliente(db, cedula)
