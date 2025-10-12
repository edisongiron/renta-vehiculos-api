from database.db import engine, meta
from .clientes import cliente
from .vehiculo import vehiculo
from .alquileres import alquileres
from .usuario import usuario
from .roles import roles
from .estado_alquiler import estado_alquiler
from .auth_usuarios import auth_usuarios

# Crear tablas solo si es necesario
# meta.create_all(engine)
