from fastapi import APIRouter
from typing import List
from controllers.Clientes.index import Clientes
from models.cliente import  ClienteResponse


router = APIRouter(prefix="/clientes", tags=["Clientes"])

# GET -> /
router.add_api_route(
    path="/",
    response_model=List[ClienteResponse],
    endpoint=Clientes.obtener_clientes,
    summary="Obtener todos los clientes",
    description="Obtiene una lista de todos los clientes registrados",
    methods=["GET"]
)


# GET -> /{cliente_id}
router.add_api_route(
    path="/{cliente_id}",
    response_model=ClienteResponse,
    endpoint=Clientes.obtener_cliente,
    summary="Obtener cliente por ID",
    description="Obtiene los detalles de un cliente específico por su ID",
    methods=["GET"]
)


# POST -> /
router.add_api_route(
    path="/",
    response_model=ClienteResponse,
    endpoint=Clientes.crear_cliente,
    status_code=201,
    summary="Crear nuevo cliente",
    description="Registra un nuevo cliente en el sistema",
    methods=["POST"]
)


# PUT -> /{cliente_id}
router.add_api_route(
    path="/{cliente_id}",
    response_model=ClienteResponse,
    endpoint=Clientes.actualizar_cliente,
    summary="Actualizar cliente",
    description="Actualiza los datos de un cliente existente",
    methods=["PUT"]
)


# DELETE -> /{cliente_id}
router.add_api_route(
    path="/{cliente_id}",
    summary="Eliminar cliente",
    endpoint=Clientes.eliminar_cliente,
    description="Elimina un cliente del sistema (solo si no tiene alquileres activos)",
    methods=["DELETE"]
)

