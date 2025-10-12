from sqlalchemy import ForeignKey, Table, Column, DateTime
from sqlalchemy.sql.sqltypes import Integer, String, Float
from database.db import meta
import uuid
from sqlalchemy.sql import func

alquileres = Table(
    "alquileres",
    meta,
    Column("id", String(36), primary_key=True, default=lambda: str(uuid.uuid4())),
    Column("fecha_inicio", String(20)),
    Column("fecha_fin", String(20)),
    Column("dias_alquiler", Integer),
    Column("precio_total", Float),
    Column("observaciones", String(255)),
    Column("fecha_devolucion_real", String(20)),
    
    # Relaciones
    Column("cliente_id", String(36), ForeignKey("cliente.id", ondelete="CASCADE")),
    Column("vehiculo_id", String(36), ForeignKey("vehiculo.id", ondelete="CASCADE")),
    Column("estado_id", Integer, ForeignKey("estado_alquiler.id", ondelete="RESTRICT"), default=1),
    
    # Campos de auditoría
    Column("creado_por", String(36), ForeignKey("auth_usuarios.id")),
    Column("actualizado_por", String(36), ForeignKey("auth_usuarios.id")),
    Column("fecha_creacion", DateTime, default=func.now()),
    Column("fecha_actualizacion", DateTime, default=func.now(), onupdate=func.now()),
)
