from sqlalchemy import Table, Column, ForeignKey, DateTime
from sqlalchemy.sql.sqltypes import String, Integer
from database.db import meta
import uuid
from sqlalchemy.sql import func

usuario = Table(
    "usuario",
    meta,
    Column("id", String(36), primary_key=True, default=lambda: str(uuid.uuid4())),
    Column("nombre", String(100)),
    Column("email", String(100), unique=True),
    Column("telefono", String(20)),
    Column("fecha_registro", String(20)),
    
    # Relación con roles
    Column("rol_id", Integer, ForeignKey("roles.id", ondelete="RESTRICT"), default=1),
    
    # Campos de auditoría
    Column("creado_por", String(36), ForeignKey("auth_usuarios.id")),
    Column("actualizado_por", String(36), ForeignKey("auth_usuarios.id")),
    Column("fecha_creacion", DateTime, default=func.now()),
    Column("fecha_actualizacion", DateTime, default=func.now(), onupdate=func.now()),
)
