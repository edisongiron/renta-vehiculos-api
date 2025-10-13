from sqlalchemy import Table, Column, ForeignKey, DateTime, Boolean
from sqlalchemy.sql.sqltypes import String, Integer
from database.db import meta
import uuid
from sqlalchemy.sql import func

auth_usuarios = Table(
    "auth_usuarios",
    meta,
    Column("id", String(36), primary_key=True, default=lambda: str(uuid.uuid4())),
    Column("username", String(50), unique=True, nullable=False),
    Column("email", String(100), unique=True, nullable=False),
    Column("password_hash", String(255), nullable=False),
    Column("nombre_completo", String(100)),
    Column("activo", Boolean, default=True),
    Column("ultimo_login", DateTime),
    
    # Relación con roles
    Column("rol_id", Integer, ForeignKey("roles.id", ondelete="RESTRICT"), default=2),  # Default user role
    
    # Campos de auditoría (self-referencing para el primer usuario admin)
    Column("creado_por", String(36), ForeignKey("auth_usuarios.id")),
    Column("actualizado_por", String(36), ForeignKey("auth_usuarios.id")),
    Column("fecha_creacion", DateTime, default=func.now()),
    Column("fecha_actualizacion", DateTime, default=func.now(), onupdate=func.now()),
)
